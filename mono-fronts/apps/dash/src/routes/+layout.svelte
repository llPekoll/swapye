<script lang="ts">
    import "../app.css";
    import { page } from "$app/stores";
    import { SvelteToast } from "@zerodevx/svelte-toast";
    import Nav from "$lib/components/Nav.svelte";
    import { dev } from "$app/environment";
    import { inject } from "@vercel/analytics";

    inject({ mode: dev ? "development" : "production" });

    let email = "";
    if ($page.data.user) {
        email = $page.data.user.email || "";
    }
    const options = {
        position: "top-right",
        duration: 3000,
        // keepOnHover: true,
        // type: "success",
    };
</script>

<nav>
    {#if $page.data.user}
        <Nav {email} />
    {/if}
</nav>

<main>
    <slot />
</main>
<SvelteToast {options} />
