import { writable } from 'svelte/store';
import type { ID } from '$lib/types';

export const identity = writable<ID>(
    {
        langs: [{
            lang: '',
            openingText: '',
            closingText: '',
        }],
        logoCompnay: '',
        closingText: '',
        openingText: '',
        color: '',
    }
);