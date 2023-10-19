import { env } from "$lib/env.js";
import { fail, redirect } from "@sveltejs/kit";
import axios from "axios";
import type { Action, Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const tradRes = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    const trads = await tradRes.json();
    if (locals.user) {
        throw redirect(302, "/games");
    }
    return {
        trads
    }
};

const login: Action = async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get("email");
    const password = data.get("password");
    const payload = {
        email,
        password,
    };
    let user;
    const url = `${env.VITE_BACKEND_DNS}/auth/login`;
    try {
        const ret = await axios.post(url, payload);
        user = await ret.data;
        console.log({ user });
    } catch (e) {
        return fail(400, { invalid: true });
    }
    cookies.set("session", user.uuid, {
        path: "/",
        httpOnly: true,
        sameSite: "strict",
        secure: process.env.NODE_ENV === "production",
        maxAge: 60 * 60 * 24 * 30,
    });
    throw redirect(302, "/games");
};

export const actions: Actions = { login };
