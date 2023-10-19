<script>
    // This is just here to show how it could be used in any component
    // with zero dependency once the styles are in your stylesheet

    export let tooltip = false; // prevent blank tooltips
</script>

<div data-tooltip={tooltip}>
    <slot />
</div>
