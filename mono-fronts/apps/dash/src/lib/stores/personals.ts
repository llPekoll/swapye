import { writable } from "svelte/store";
import type { Personals } from "$lib/types";

export const personals = writable<Personals>({
    name: '',
    address: '',
    postal: '',
    phone: '',
    siret: '',
    rib: '',
    company_name: '',
    conact_email: '',
    city: '',

});