<script>
    import { page } from "$app/stores";
</script>

<section
    class="text-3xl flex items-center justify-center text-red-500 align-middle h-screen"
>
    <div>
        <h1 class="text-center">Oops!</h1>
        <p>
            {@html $page.error.message}
        </p>
    </div>
</section>
