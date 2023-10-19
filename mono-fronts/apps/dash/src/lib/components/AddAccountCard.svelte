<script lang="ts">
    import { page } from "$app/stores";
    const traduction = $page.data.user.traduction;
</script>

<div class=" rounded-lg flex items-center justify-center">
    <p class="text-gray-700 text-7xl">
        {@html traduction.icon_add_account}
    </p>
</div>
