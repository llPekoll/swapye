<script>
    import "../app.css";
    import { dev } from "$app/environment";
    import { inject } from "@vercel/analytics";
    import { SvelteToast } from "@zerodevx/svelte-toast";

    const options = {
        position: "top-right",
        duration: 3000,
    };
    inject({ mode: dev ? "development" : "production" });
</script>

<slot />

<SvelteToast {options} />
