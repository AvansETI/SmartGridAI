import { OccupantsActivity } from "@/enums/occupants-activity";


export function occupantsActivityFilter(value: number): string {

    //@TODO: I18N
    switch (value) {

        case OccupantsActivity.NA:
            return "N/A";

        case OccupantsActivity.READ:
            return "Occupant(s) will be reading";

        case OccupantsActivity.STAND:
            return "Occupant(s) will be standing";

        case OccupantsActivity.WALK:
            return "Occupant(s) will be walking";

        case OccupantsActivity.WORK:
            return "Occupant(s) will be working";
    }

    return "-";
}
