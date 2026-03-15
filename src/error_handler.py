from dash_iconify import DashIconify


class ErrorHandler:
    @staticmethod
    def build_error_notification(message: str) -> list[dict]:
        return [
            dict(
                title="Whoops!",
                id="show-notify",
                action="show",
                message=message,
                icon=DashIconify(icon="tabler:face-id-error"),
            )
        ]

    @staticmethod
    def sync_selected_countries(backend_game, hideout: dict) -> dict:
        if backend_game.chosen_country_1:
            hideout["selected"] = (
                [backend_game.chosen_country_1.name, backend_game.chosen_country_2.name]
                if backend_game.chosen_country_2
                else [backend_game.chosen_country_1.name]
            )
        else:
            hideout["selected"] = []
        return hideout

    @staticmethod
    def invalid_attacker_notifications(backend_game, country) -> list[dict]:
        if country.owner != backend_game.active_player:
            return ErrorHandler.build_error_notification(
                "You cannot attack with a country that you do not own!"
            )

        if country.dict_of_attributes[backend_game.current_attribute.name].rank == 0:
            return ErrorHandler.build_error_notification(
                "Uh-oh! This country has no data for the current attribute!"
            )

        return []

    @staticmethod
    def validate_second_country_selection(backend_game, country) -> tuple[bool, list[dict], bool]:
        if (
            backend_game.peacemode
            and country.owner.name != "Nobody"
            and country.owner != backend_game.active_player
        ):
            return False, ErrorHandler.build_error_notification(
                "You can not attack another player's countries in peace mode! Choose another country!"
            ), True

        if not country.is_connected_with(backend_game.chosen_country_1):
            return False, ErrorHandler.build_error_notification(
                "These countries don't share a border! Choose another pair!"
            ), True

        if country.owner == backend_game.active_player:
            return False, ErrorHandler.build_error_notification(
                "You already own this country!"
            ), False

        if country.dict_of_attributes[backend_game.current_attribute.name].rank == 0:
            return False, ErrorHandler.build_error_notification(
                "Uh-oh! This country has no data for the current attribute!"
            ), False

        return True, [], False
