<script lang="ts">
    export let type: string = "text";
    export let name: string = "José Martins";
    export let classes: string = "";
    export let value: string = "";
    export let needsUpdate: boolean = false;
</script>

<input
    on:click={() => (needsUpdate = true)}
    on:keypress={() => (needsUpdate = true)}
    {type}
    {name}
    class={classes}
    {value}
/>
