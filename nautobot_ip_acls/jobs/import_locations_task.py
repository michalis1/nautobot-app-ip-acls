"""Nautobot Job to import location based on CSV data input."""

from nautobot.apps.jobs import Job, register_jobs, TextVar
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status

import csv
import io
from itertools import chain


name = "Import Locations from CSV"

# Expected Columns to validate CSV data
EXPECTED_COLUMNS = ["name", "city", "state"]

# Name of Sites suffix
SITE_NAME_SUFFIX = ["DC", "BR"]

# Site Statuses
STATUS_ACTIVE = Status.objects.get(name="Active")

def validate_csv(logger, csv_data, expected_columns):
    """ Validate that the data have a valid CSV format based on the requirements."""

    # Get the header row
    header_str = csv_data.splitlines()[0]

    # Parse header into a list of strings
    header = [column_header.strip() for column_header in header_str.split(",")]

    # Check if the header matches the expected columns
    if header != expected_columns:
        logger.error(f"Invalid header. Expected: {expected_columns}, Found: {header}")
        return False
    
    # Validate each row for the correct number of fields
    for row_number, row in enumerate(csv_data.splitlines()[1:], start=2):
        row_data = row.split(',')
        if len(row_data) != len(expected_columns) or "" in row_data:
            logger.error(f"Invalid row at line {row_number}: {row}")
            return False
        else:
            site, city, state = row_data
            if site[-2:] not in SITE_NAME_SUFFIX:
                logger.error(f"{site} on {row} at line {row_number}: The name of the site should ends with one of the following options: {SITE_NAME_SUFFIX}")
                return False
            if (len(state)<=2):
                logger.error(
                    f"{state} on {row} at line {row_number}: The name of the state should be the full state name, no two character abbreviations should be used."
                )
                return False

        
    logger.info("CSV data are valid.")
    return True

def update_or_create_location(logger, location_name, location_type, parent):
    """ Create or Update a Location nautobot object """

    created = False
    updated = False

    # Get or create the Location
    try:
        location = Location.objects.get(name=location_name)
    except Location.DoesNotExist:
        location = Location(
            name = location_name,
            status = STATUS_ACTIVE,
            location_type = LocationType.objects.get(name=location_type)
        )
        created = True

    # If the location wasn't created check if it needs to be updates
    if not created:
        if location.parent != parent:
            location.parent = parent
            updated = True
        if location.location_type.name != location_type:
            location.location_type = LocationType.objects.get(name=location_type)
            updated = True
        if updated:
            location.validated_save()
            logger.info(msg=f"Location {location.name} has been updated.", extra={"object": location})
        else:
            logger.info(msg=f"Location {location.name} has remained unchanged.", extra={"object": location})
    else:
        location.parent = parent
        location.location_type = LocationType.objects.get(name=location_type)
        location.validated_save()
        logger.info(msg=f"Location {location.name} has been created.", extra={"object": location})

    return location, created


class ImportLocations(Job):

    csv_data = TextVar(
        label = "CSV Data",
        default = "name, city, state",
        widget="textarea",
        required = True,
    )

    class Meta:
        """Metadata describing this job."""

        name = "Import Locations from CSV"
        description = "Import Locations from CSV-formatted data."
        has_sensitive_variables = False

    def run(self, csv_data):

        if validate_csv(self.logger, csv_data.strip(), EXPECTED_COLUMNS):

            # Create a CSV like file from String
            csv_file = io.StringIO(csv_data.strip())

            # Parse CSV file into a list of dicts
            locations_csv = list(csv.DictReader(csv_file))

            # Get the states in a set
            states = {
                (location['state'].strip(), None, "State") 
                for location in locations_csv
            }

            # Get the cities in a set
            cities = {
                (location['city'].strip(),location['state'].strip(), "City") 
                for location in locations_csv
            }

            # Get the sites in a set
            sites = {
                (
                    location['name'].strip(),
                    location['city'].strip(),
                    "Data Center" if location['name'].strip()[-2:]=="DC" else "Branch"
                ) 
                for location in locations_csv
            }

            # iterate over States, Cities, Sites to update or create them
            for location_name, location_parent, location_type in chain(states, cities, sites):
                location_obj, _ = update_or_create_location(
                        logger = self.logger, 
                        location_name = location_name, 
                        location_type = location_type,
                        parent = Location.objects.get(name=location_parent) if location_parent else None
                    )
        else:
            self.logger.error("CSV data are not valid.")

register_jobs(ImportLocations)
