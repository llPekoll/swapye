interface TypesNskins {
    types: GameType[];
    skins: Skin[];
}
interface GameType {
    id: number;
    name: string;
    ref_id: number;
}
interface Skin {
    id: number;
    name: string;
    game: number;
    ref_id: number;
}

export type { TypesNskins, GameType, Skin }