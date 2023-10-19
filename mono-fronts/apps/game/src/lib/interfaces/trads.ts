
export interface TradDefaults {
    email: string,
    phone: string,
    rules: string,
    lost: string,
    cross: string,
    cant_replay: string,
    no_more_play_today: string,
    no_more_play: string,
    address: string,
    name: string,
    policy: string,
    postal: string,
    submit: string
}

export interface TradIntroOutro {
    openingText: string;
    closingText: string;

}
export interface TradPrices {
    name: string,
    img: string,
    priceId: number,
}

export type Trads = {
    [key in '🇫🇷 France' | '🇬🇧 Anglais' | '🇪🇸 Espagnol' | "🇮🇹 Italien" | "🇩🇪 Allemand" | "🇨🇳 Chinois"]:
    {
        tradDefaults: TradDefaults,
        tradIntroOutro: TradIntroOutro,
        tradPrices: TradPrices[],
        langs: string[]
    };
};


