// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces

import type { Trads } from "$lib/utils";

// and what to do when importing types
declare namespace App {
    interface Locals {
        user: {
            email: string;
            uuid: string;
            rights: string[];
            traduction: Trads;
        };
        typesNSkins: {
            types: string[];
            skins: string[];
        };
    }
    // interface PageData {
    //     trads: Trads;
    // }
    // interface Error {}
    // interface Platform {}
}
