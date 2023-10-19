import { writable } from 'svelte/store';
import type { DryRun } from '$lib/types';

export const dryRun = writable<DryRun>(
    {
        forceResultWon: false,
        forceResultLost: false,
        forceResultCantReplay: false,
        forceResultCantReplayToday: false,
        dryRun: false,
    }
);