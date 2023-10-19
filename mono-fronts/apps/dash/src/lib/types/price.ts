import type { TimeTable } from "./timeTable";
interface TradPack {
    lang: string,
    src: string,
    name: string,
}
export interface Price {
    name: string;
    number: number;
    img: File | string;
    id: number;
    displayPriceName: boolean;
    emailTemplate: number;
    timetable: TimeTable[];
    consolationPrice: boolean;
    price_won?: number;
    extra_langs: string[];
    tradPacks: TradPack[]
}
