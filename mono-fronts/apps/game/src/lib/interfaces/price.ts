export interface Price {
    name: string;
    number: number;
    img: File | string;
    id: number;
    display_price_name: boolean;
    offset_price_name: boolean;
    email_template: number;
    price_left?: number;
}
