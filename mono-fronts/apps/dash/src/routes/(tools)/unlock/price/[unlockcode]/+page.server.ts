import { env } from "$lib/env.js";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const priceRes = await fetch(
        `${env.VITE_BACKEND_DNS}/unlock/price/${params.unlockcode}`
    );
    const result = await priceRes.json();
    return {
        result
    };
};
