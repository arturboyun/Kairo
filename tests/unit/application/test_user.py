import pytest
from unittest.mock import Mock
from uuid import UUID
from uuid_extensions import uuid7

from kairo.application.dto.user import CreateUserDTO, GetUserByIdQuery
from kairo.application.interactors.user import CreateUserUseCase, GetUserByIdUseCase
from kairo.domain.entities.user import User
from kairo.domain.exceptions import DomainError
from kairo.domain.gateways.user_gateway import UserGateway, UserReader


class TestGetUserByIdUseCase:
    """Test suite for GetUserByIdUseCase."""

    @pytest.fixture
    def mock_user_reader(self):
        """Mock user reader fixture."""
        return Mock(spec=UserReader)

    @pytest.fixture
    def get_user_by_id_use_case(self, mock_user_reader):
        """GetUserByIdUseCase instance with mocked dependencies."""
        return GetUserByIdUseCase(mock_user_reader)

    @pytest.fixture
    def user_id(self):
        """Valid user ID fixture."""
        return uuid7()

    @pytest.fixture
    def get_user_query(self, user_id):
        """GetUserByIdQuery fixture."""
        return GetUserByIdQuery(user_id=user_id)

    @pytest.fixture
    def mock_user(self, user_id):
        """Mock user entity fixture."""
        return User(
            id=user_id,
            email="test@example.com",
            username="testuser",
            password="password123"
        )

    def test_get_user_by_id_success(self, get_user_by_id_use_case, mock_user_reader, get_user_query, mock_user):
        """Test successful user retrieval by ID."""
        # Arrange
        mock_user_reader.get_by_id.return_value = mock_user

        # Act
        result = get_user_by_id_use_case(get_user_query)

        # Assert
        assert result == mock_user
        mock_user_reader.get_by_id.assert_called_once_with(get_user_query.user_id)

    def test_get_user_by_id_not_found(self, get_user_by_id_use_case, mock_user_reader, get_user_query):
        """Test user retrieval when user does not exist."""
        # Arrange
        mock_user_reader.get_by_id.return_value = None

        # Act
        result = get_user_by_id_use_case(get_user_query)

        # Assert
        assert result is None
        mock_user_reader.get_by_id.assert_called_once_with(get_user_query.user_id)

    def test_get_user_by_id_with_different_user_ids(self, get_user_by_id_use_case, mock_user_reader):
        """Test user retrieval with different user IDs."""
        # Arrange
        user_id_1 = uuid7()
        user_id_2 = uuid7()
        query_1 = GetUserByIdQuery(user_id=user_id_1)
        query_2 = GetUserByIdQuery(user_id=user_id_2)
        
        user_1 = User(
            id=user_id_1,
            email="user1@example.com",
            username="user1",
            password="password123"
        )
        user_2 = User(
            id=user_id_2,
            email="user2@example.com",
            username="user2",
            password="password456"
        )
        
        mock_user_reader.get_by_id.side_effect = lambda uid: user_1 if uid == user_id_1 else user_2

        # Act
        result_1 = get_user_by_id_use_case(query_1)
        result_2 = get_user_by_id_use_case(query_2)

        # Assert
        assert result_1 == user_1
        assert result_2 == user_2
        assert mock_user_reader.get_by_id.call_count == 2

    def test_get_user_by_id_query_immutability(self, user_id):
        """Test that GetUserByIdQuery is immutable (frozen dataclass)."""
        query = GetUserByIdQuery(user_id=user_id)
        
        with pytest.raises(AttributeError):
            query.user_id = uuid7()  # Should raise an error since the dataclass is frozen

    def test_get_user_by_id_use_case_stores_user_reader(self, mock_user_reader):
        """Test that the use case correctly stores the user reader dependency."""
        # Act
        use_case = GetUserByIdUseCase(mock_user_reader)
        
        # Assert
        assert use_case._user_reader is mock_user_reader


class TestCreateUserUseCase:
    """Test suite for CreateUserUseCase."""

    @pytest.fixture
    def mock_user_gateway(self):
        """Mock user gateway fixture."""
        return Mock(spec=UserGateway)

    @pytest.fixture
    def create_user_use_case(self, mock_user_gateway):
        """CreateUserUseCase instance with mocked dependencies."""
        return CreateUserUseCase(mock_user_gateway)

    @pytest.fixture
    def valid_user_dto(self):
        """Valid CreateUserDTO fixture."""
        return CreateUserDTO(
            email="test@example.com",
            username="testuser",
            password="password123"
        )

    @pytest.fixture
    def mock_user(self):
        """Mock user entity fixture."""
        return User(
            email="test@example.com",
            username="testuser",
            password="password123"
        )

    def test_create_user_success(self, create_user_use_case, mock_user_gateway, valid_user_dto, mock_user):
        """Test successful user creation."""
        # Arrange
        mock_user_gateway.get_by_email.return_value = None
        mock_user_gateway.get_by_username.return_value = None
        mock_user_gateway.create.return_value = mock_user

        # Act
        result = create_user_use_case(valid_user_dto)

        # Assert
        assert result == mock_user
        mock_user_gateway.get_by_email.assert_called_once_with("test@example.com")
        mock_user_gateway.get_by_username.assert_called_once_with("testuser")
        mock_user_gateway.create.assert_called_once()
        
        # Verify the user passed to create has the correct attributes
        created_user = mock_user_gateway.create.call_args[0][0]
        assert created_user.email == "test@example.com"
        assert created_user.username == "testuser"
        assert created_user.password == "password123"
        assert isinstance(created_user.id, UUID)

    def test_create_user_email_already_exists(self, create_user_use_case, mock_user_gateway, valid_user_dto, mock_user):
        """Test user creation fails when email already exists."""
        # Arrange
        mock_user_gateway.get_by_email.return_value = mock_user
        mock_user_gateway.get_by_username.return_value = None

        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            create_user_use_case(valid_user_dto)
        
        assert str(exc_info.value) == "User with email 'test@example.com' already exists."
        mock_user_gateway.get_by_email.assert_called_once_with("test@example.com")
        mock_user_gateway.get_by_username.assert_not_called()
        mock_user_gateway.create.assert_not_called()

    def test_create_user_username_already_exists(self, create_user_use_case, mock_user_gateway, valid_user_dto, mock_user):
        """Test user creation fails when username already exists."""
        # Arrange
        mock_user_gateway.get_by_email.return_value = None
        mock_user_gateway.get_by_username.return_value = mock_user

        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            create_user_use_case(valid_user_dto)
        
        assert str(exc_info.value) == "User with username 'testuser' already exists."
        mock_user_gateway.get_by_email.assert_called_once_with("test@example.com")
        mock_user_gateway.get_by_username.assert_called_once_with("testuser")
        mock_user_gateway.create.assert_not_called()

    def test_create_user_both_email_and_username_exist(self, create_user_use_case, mock_user_gateway, valid_user_dto, mock_user):
        """Test user creation fails when both email and username already exist - email check happens first."""
        # Arrange
        mock_user_gateway.get_by_email.return_value = mock_user
        mock_user_gateway.get_by_username.return_value = mock_user

        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            create_user_use_case(valid_user_dto)
        
        assert str(exc_info.value) == "User with email 'test@example.com' already exists."
        mock_user_gateway.get_by_email.assert_called_once_with("test@example.com")
        mock_user_gateway.get_by_username.assert_not_called()
        mock_user_gateway.create.assert_not_called()

    def test_create_user_with_different_emails(self, create_user_use_case, mock_user_gateway, mock_user):
        """Test user creation with different email addresses."""
        # Arrange
        user_dto = CreateUserDTO(
            email="another@example.com",
            username="anotheruser",
            password="password456"
        )
        mock_user_gateway.get_by_email.return_value = None
        mock_user_gateway.get_by_username.return_value = None
        mock_user_gateway.create.return_value = mock_user

        # Act
        result = create_user_use_case(user_dto)

        # Assert
        assert result == mock_user
        mock_user_gateway.get_by_email.assert_called_once_with("another@example.com")
        mock_user_gateway.get_by_username.assert_called_once_with("anotheruser")

    def test_create_user_gateway_create_called_with_user_entity(self, create_user_use_case, mock_user_gateway, valid_user_dto, mock_user):
        """Test that the gateway create method is called with a User entity."""
        # Arrange
        mock_user_gateway.get_by_email.return_value = None
        mock_user_gateway.get_by_username.return_value = None
        mock_user_gateway.create.return_value = mock_user

        # Act
        create_user_use_case(valid_user_dto)

        # Assert
        mock_user_gateway.create.assert_called_once()
        created_user_arg = mock_user_gateway.create.call_args[0][0]
        assert isinstance(created_user_arg, User)
        assert created_user_arg.email == valid_user_dto.email
        assert created_user_arg.username == valid_user_dto.username
        assert created_user_arg.password == valid_user_dto.password
