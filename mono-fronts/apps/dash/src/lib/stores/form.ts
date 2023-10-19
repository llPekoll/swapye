import { writable } from 'svelte/store';
import type { FormPart } from '$lib/types';

export const forms = writable<FormPart>(
    {
        formPortrait: '',
        formLandscape: '',
    }
);