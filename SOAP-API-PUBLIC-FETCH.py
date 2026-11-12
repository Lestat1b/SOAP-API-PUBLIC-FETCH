"""
Football Pool SOAP Consumer
---------------------------
Consumes the public Football Pool Information SOAP service.

This program:
1. Connects to a public WSDL using Zeep.
2. Retrieves team names from the SOAP service.
3. Converts the SOAP response into native Python objects.
4. Validates a user-supplied team name.
5. Generates custom error messages when validation fails.
"""

from zeep import Client, helpers


# ------------------------------------------------------------------
# Public WSDL selected from the course document:
# "Public SOAP Web Services for Interoperability Application"

WSDL_URL = "https://footballpool.dataflex.dev/info.wso?WSDL"


# ------------------------------------------------------------------
def get_soap_client():
    """
    Create and return the Zeep SOAP client.
    """

    return Client(wsdl=WSDL_URL)


# ------------------------------------------------------------------
def get_team_names():
    """
    Call the TeamNames SOAP operation.

    Zeep receives the XML SOAP response and converts it into
    a Python-compatible object. helpers.serialize_object()
    converts it into standard Python data.
    """

    try:
        client = get_soap_client()

        # Call the public SOAP operation.
        response = client.service.TeamNames()

        # Convert the Zeep object into native Python data.
        teams = helpers.serialize_object(response)

        return teams

    except Exception as exc:
        raise RuntimeError(
            f"SOAP service request failed: {exc}"
        )


# ------------------------------------------------------------------
def validate_team(team_name):
    """
    Validate the team name.

    Rules:
    1. A team name must be supplied.
    2. It must contain letters.
    3. It must match one of the team names returned
       by the public SOAP service.

    Matching is case-insensitive.
    """

    if team_name is None or str(team_name).strip() == "":
        raise ValueError(
            "Validation error: a team name is required."
        )

    team_name = str(team_name).strip()

    if not any(character.isalpha() for character in team_name):
        raise ValueError(
            f"Validation error: '{team_name}' must contain letters."
        )

    # Get the valid options from the SOAP service.
    teams = get_team_names()

    if not teams:
        raise ValueError(
            "Validation error: the SOAP service returned no team names."
        )

    # Create a case-insensitive lookup.
    team_lookup = {
        str(team).strip().lower(): str(team).strip()
        for team in teams
    }

    normalized_name = team_name.lower()

    if normalized_name not in team_lookup:
        raise ValueError(
            f"Validation error: '{team_name}' is not in "
            f"the list of valid team names."
        )

    # Return the correctly formatted name supplied by SOAP.
    return team_lookup[normalized_name]


# ------------------------------------------------------------------
def get_team_information(team_name):
    """
    Validate a team and retrieve information about that team
    from the public SOAP service.
    """

    try:
        # Validate against TeamNames().
        valid_team = validate_team(team_name)

        client = get_soap_client()

        # Teams searches for teams containing the supplied name.
        response = client.service.Teams(
            sTeamName=valid_team
        )

        # Convert Zeep SOAP object to native Python objects.
        team_data = helpers.serialize_object(response)

        return {
            "team": valid_team,
            "information": team_data
        }

    except ValueError as exc:

        # Custom error + original exception text {exc}.
        raise ValueError(
            f"Team validation failed: {exc}"
        )

    except Exception as exc:
        raise RuntimeError(
            f"SOAP service request failed: {exc}"
        )


# ------------------------------------------------------------------
if __name__ == "__main__":

    try:
        print("Soccer Rankings")
        print("-------------------------")

        team = input("Enter a team name: ")

        result = get_team_information(team)

        print("\nTeam Information")
        print("----------------")

        print(f"Team: {result['team']}")

        print("\nSOAP Data:")

        information = result["information"]

        if isinstance(information, list):
            for item in information:
                print(item)
        else:
            print(information)

    except Exception as exc:

        print(
            f"Something went wrong while processing "
            f"the SOAP request: {exc}"
        )