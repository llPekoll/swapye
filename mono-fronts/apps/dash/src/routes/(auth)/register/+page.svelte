<script lang="ts">
    import type { ActionData, PageData } from "./$types";
    import { goto, invalidateAll } from "$app/navigation";
    import { page } from "$app/stores";

    import { applyAction, enhance } from "$app/forms";

    export let form: ActionData;
    // export let data: PageData;
    const traduction = $page.data.user.traduction;
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let disabled = false;
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div
        class="px-8 py-6 mx-4 mt-4 text-left bg-white shadow-lg md:w-4/5 lg:w-1/2 w-full"
    >
        <div class="flex justify-center">
            <img src={traduction.logo_swapye_couleur} alt="logo" class="w-14" />
        </div>
        <h3 class="text-2xl font-bold text-center">
            {traduction.join_us_plus}
        </h3>
        <form
            method="POST"
            action="?/register"
            use:enhance={({ form }) => {
                submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
                submitColor = "bleu-gris/[.3]";
                cursor = "cursor-not-allowed";
                disabled = true;
                return async ({ result, update }) => {
                    // @ts-ignore
                    if (result.data?.invalid) {
                        cursor = "cursor-pointer";
                        submitText = traduction.submit;
                        submitColor = "bleu-gris";
                        disabled = false;
                        return;
                    }
                    await applyAction(result);
                    await invalidateAll();
                    goto("/login");
                };
            }}
        >
            <div class="mt-4">
                <div>
                    <div class="mt-4">
                        <label class="block" for="email"
                            >{traduction.email_tip}</label
                        >
                        <input
                            data-test="email"
                            name="email"
                            type="email"
                            placeholder="Email"
                            class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                        />
                    </div>
                    {#if form?.user}
                        <p class="text-xs text-red-400 ml-3">
                            {traduction.please_change_email}
                        </p>
                    {/if}

                    <div class="mt-4">
                        <label class="block" for="password"
                            >{traduction.password}</label
                        >
                        <input
                            data-test="password"
                            name="password"
                            type="password"
                            placeholder="Password"
                            class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                        />
                    </div>
                    <div class="mt-4">
                        <label class="block" for="password_confirm"
                            >{traduction.confirm_password}</label
                        >
                        <input
                            data-test="password_confirm"
                            name="password_confirm"
                            type="password"
                            placeholder="Password"
                            class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                        />
                    </div>
                    {#if form?.pass}
                        <p class="text-xs text-red-400 ml-3">
                            {traduction.pass_not_mach}
                        </p>
                    {/if}
                    {#if form?.long}
                        <p class="text-xs text-red-400 ml-3">
                            {traduction.more_char_for_pass}
                        </p>
                    {/if}

                    <button
                        data-test="submit"
                        type="submit"
                        {disabled}
                        class=" py-2 text-white bg-{submitColor} rounded-lg w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor} items-center justify-center text-center mx-auto"
                        >{@html submitText}</button
                    >
                    <div class="mt-6 text-grey-dark">
                        {traduction.alreadry_have_account}
                        <a class="text-blue-600 hover:underline" href="/login">
                            {traduction.login}
                        </a>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
