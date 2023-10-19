import { redirect } from "@sveltejs/kit";

import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ cookies }) => {
    // cookies.set("session", "", {
    //     path: "/",
    //     expires: new Date(0),
    // });
    throw redirect(302, "/login");
};

export const actions: Actions = {
    default({ cookies }) {
        // @ts-ignore
        cookies.set("session", "", {
            path: "/",
            expires: new Date(0),
        });
        throw redirect(302, "/login");
    },
};
