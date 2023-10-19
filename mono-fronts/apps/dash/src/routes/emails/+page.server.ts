import { env } from "$lib/env.js";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const res = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    // const res2 = await fetch(`${env.VITE_BACKEND_DNS}/emails`, {
    // 	headers: {
    // 		session: locals.user.uuid,
    // 		Accept: 'application/json',
    // 		'Content-Type': 'application/json'
    // 	}
    // });
    // const leads = await res2.json();
    const trads = await res.json();
    return {
        trads,
        // leads,
    };
};
