class AppConfig:
    host: str = "0.0.0.0"
    port: int = 8000


class DBConfig:
    user: str = "notes_boards_user"
    password: str = "notes_boards_pass"
    host: str = "db"
    port: int = 5432
    db_name: str = "notes_boards"
