<script lang="ts">
    import { onMount } from "svelte";
    export let src = "";
    export let alt = "";
    export let className = "";

    let loaded = false;

    onMount(() => {
        const img = new Image();
        img.src = src;
        img.onload = () => {
            loaded = true;
        };
    });
</script>

{#if loaded}
    <img class={className} {src} {alt} />
{/if}

<style>
    img {
        pointer-events: none;
    }
</style>
