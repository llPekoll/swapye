export interface DateNRegion {
    startDate: Date;
    endDate: Date;
    startHour: string;
    endHour: string;
    unlimitedInTime: boolean;
    losingFactor: number;
    timeZone: string;
    disableDates: false;
    startSateToDisp: string;
    endSateToDisp: string;
    startHourToDisp: string;
    endHourToDisp: string;
    extraLangs: { lang: string }[];
}
