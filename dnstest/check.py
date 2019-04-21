from .matches import load


class Check:

    def __init__(self, name=None, record=None, matches=None):
        """
        Stores the passed in kwargs on our instance
        """
        self.name = name
        self.record = record

        # Map our matches into the corresponding match classes
        self.matches = list(map(load, matches))

    def records(self, resolver):
        """
        Returns the records for this check
        """
        return resolver.query(
            domain=self.record['domain'],
            query_type=self.record['type']
        )

    def __call__(self, resolver):
        """
        Yields any matches that fail or None for each successful match
        """
        records = self.records(resolver)

        for match in self.matches:

            # Apply the test to every record
            success = filter(match, records)

            # Return this match if no records passed any tests
            # or return None if any of the records passed
            yield match if not any(success) else None

    def __str__(self):
        """
        Returns a string representation of this check
        """
        # Return our overridden name if set
        if self.name:
            return self.name

        # Our default representation is the domain followed by the record type
        return '{} {}'.format(self.record['domain'], self.record['type'])
