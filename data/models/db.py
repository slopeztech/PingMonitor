from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    BooleanField,
    IntegerField,
    TextField,
    DateTimeField
)
from datetime import datetime


class PingMonitorDB:
    def __init__(self, database_path: str):
        """
        Initialize the database connection.

        Args:
            database_path (str): Path to the SQLite database file
        """
        self.db = SqliteDatabase(database_path)
        # Set the database for the PingResult model
        self.PingResult._meta.database = self.db
        self.initialize_db()

    def initialize_db(self):
        """
        Initialize the database and create tables.
        """
        self.db.connect()
        self.db.create_tables([self.PingResult], safe=True)
        self.db.close()

    class PingResult(Model):
        """
        Model to store ping results.
        """
        # Site information
        site = CharField()  # The hostname or IP being pinged
        protocol = CharField()  # The protocol used (icmp, http, dns, etc.)

        # Ping results
        success = BooleanField()  # Whether the ping was successful
        response_time_ms = IntegerField(null=True)  # Response time in milliseconds
        error_message = TextField(null=True)  # Error message if the ping failed

        # Metadata
        timestamp = DateTimeField(default=datetime.now)  # When the ping was performed
        raw_output = TextField()  # Raw output from the ping command
        hostname = CharField()  # The hostname of the machine performing the ping

        class Meta:
            indexes = (
                (('site', 'protocol', 'timestamp'), True),  # Index for efficient querying
            )

        def __str__(self):
            return f"Ping to {self.site} at {self.timestamp} - {'Success' if self.success else 'Failed'}"

    def store_ping_result(self, site: str, protocol: str, result: dict):
        """
        Store a ping result in the database.

        Args:
            site (str): The hostname or IP that was pinged
            protocol (str): The protocol used for the ping
            result (dict): The result dictionary from the ping operation
        """
        try:
            with self.db.atomic():
                self.PingResult.create(
                    site=site,
                    protocol=protocol,
                    success=result.get('success', False),
                    response_time_ms=result.get('response_time_ms'),
                    error_message=result.get('error'),
                    raw_output=result.get('output', ''),
                    hostname=result.get('hostname', 'unknown')
                )
        except Exception as e:
            print(f"Error storing ping result: {e}")

    def get_ping_history(self, site: str = None, protocol: str = None, limit: int = 100):
        """
        Retrieve ping history from the database.

        Args:
            site (str, optional): Filter by site
            protocol (str, optional): Filter by protocol
            limit (int, optional): Maximum number of results to return

        Returns:
            list: List of PingResult objects
        """
        query = self.PingResult.select()

        if site:
            query = query.where(self.PingResult.site == site)
        if protocol:
            query = query.where(self.PingResult.protocol == protocol)

        return query.order_by(self.PingResult.timestamp.desc()).limit(limit)
