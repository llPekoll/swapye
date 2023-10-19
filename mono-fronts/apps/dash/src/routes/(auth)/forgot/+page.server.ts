import { env } from "$lib/env.js";
import axios from "axios";
import type { Actions, Action, PageServerLoad } from "./$types";
import { fail, redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ locals }) => {
    const tradRes = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    const trads = await tradRes.json();

    return {
        trads
    }
};

const forgot: Action = async ({ request }) => {
    console.log("forgot");
    const data = await request.formData();
    const payload = {
        email: data.get("email"),
    };
    const url = `${env.VITE_BACKEND_DNS}/auth/forgot`;
    try {
        await axios.post(url, payload);
    } catch (e) {
        return fail(400, { email: true });
    }
    throw redirect(302, "/login");
};

export const actions: Actions = {
    forgot,
};
