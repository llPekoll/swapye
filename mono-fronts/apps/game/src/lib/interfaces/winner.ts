export interface Winner {
    price?: number;
    state: 'lost' | 'won' | 'cant_replay' | 'cant_replay_today';
    img?: string;
    name?: string;
    displayTitle?: boolean;
    offsetTitle?: string;
    dayNumber: number;
}
