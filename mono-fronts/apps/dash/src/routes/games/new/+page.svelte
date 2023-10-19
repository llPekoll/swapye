<script lang="ts">
    import GameCreation from "../components/GameCreation.svelte";
    import { page } from "$app/stores";
    import type { TypesNskins } from "$lib/types";

    const typesNskins: TypesNskins = $page.data.user.typesNskins;
    console.log(typesNskins);
</script>

<section class="ml-52 pr-10 mt-10">
    <GameCreation {typesNskins} />
</section>
