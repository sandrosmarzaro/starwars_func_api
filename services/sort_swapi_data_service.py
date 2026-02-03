from typing import Any

from schemas.swapi_query_params_schema import SortOrder


class SortSwapiDataService:
    def sort(
        self,
        data: dict[str, Any],
        sort_by: str,
        sort_order: SortOrder,
    ) -> dict[str, Any]:
        if 'results' not in data:
            return data

        data['results'] = self._sort_results(
            data['results'], sort_by, sort_order
        )
        return data

    def _sort_results(
        self,
        results: list[dict[str, Any]],
        sort_by: str,
        sort_order: SortOrder,
    ) -> list[dict[str, Any]]:
        invalid_values = {None, 'unknown', 'n/a'}

        def sort_key(item: dict[str, Any]) -> float | str:
            value = item.get(sort_by, '')
            if isinstance(value, str):
                try:
                    return float(value.replace(',', ''))
                except ValueError:
                    return value.lower()
            return float(value) if value is not None else 0.0

        valid_items: list[dict[str, Any]] = []
        invalid_items: list[dict[str, Any]] = []
        for item in results:
            if item.get(sort_by) in invalid_values:
                invalid_items.append(item)
            else:
                valid_items.append(item)

        is_descending = sort_order == SortOrder.DESC
        sorted_valid = sorted(valid_items, key=sort_key, reverse=is_descending)

        return sorted_valid + invalid_items
