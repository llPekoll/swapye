import { env } from "$lib/env.js";
import { fail, redirect } from "@sveltejs/kit";
import axios from "axios";
import type { Action, Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    if (locals.user) {
        throw redirect(302, "/games");
    }
    const tradRes = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    const trads = await tradRes.json();

    return {
        trads
    }

};

const register: Action = async ({ request }) => {
    const data = await request.formData();
    const resp = await fetch(`${env.VITE_BACKEND_DNS}/auth/email_checker`, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: data.get("email") }),
    });
    if (!resp.ok) {
        return fail(400, { user: true });
    }
    if (data.get("password") !== data.get("password_confirm")) {
        return fail(400, { password: true });
    }
    if (data.get("password") !== null) {
        if (data.get("password")!.length < 3) {
            return fail(400, { long: true });
        }
    }
    const payload = {
        email: data.get("email"),
        password: data.get("password"),
    };
    const url = `${env.VITE_BACKEND_DNS}/auth/register`;
    try {
        await axios.post(url, payload);
        throw redirect(302, "/login");
    } catch (error) {
        console.log(error);
    }
};

export const actions: Actions = { register };
