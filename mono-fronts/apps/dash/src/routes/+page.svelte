<section>
    <p>you are not loged in</p>
    <form action="/logout" method="POST">
        <ul class="py-10">
            <li class="mx-3"><a href="/login" title="login">login</a></li>
            <li class="mx-3">
                <a href="/register" title="register">register</a>
            </li>
            <li class="mx-3">
                <a href="/forgot" title="password forgotten"
                    >password forgotten</a
                >
            </li>
            <li class="mx-3 inline">
                <a href="/logout" title="logout">logout</a>
            </li>
        </ul>
    </form>
</section>

<style>
    section {
        font-family: "Raleway", sans-serif;
        text-align: center;
        background-color: #3d516d;
        font-size: 14px;
        padding: 50px;
        height: 100vh;
    }
    a:link,
    a:visited,
    a:active {
        color: white;
        text-decoration: none;
    }
    ul li {
        position: relative;
        display: inline-block;
        overflow: hidden;
    }
    ul li:hover,
    ul li:focus {
        outline: none;
    }
    ul li a {
        position: relative;
        display: inline-block;
        color: #fff;
        font-size: 1.5em;
        text-decoration: none;
        text-transform: uppercase;
        font-weight: 700;
        transition: transform 0.5s ease;
        -webkit-transition: transform 0.5s ease;
    }
    ul li a:before {
        position: absolute;
        top: 100%;
        content: attr(title); /* The selector for Wordpress */
        color: #333;
        -webkit-transform: translate3d(0, 0, 0);
        -moz-transform: translate3d(0, 0, 0);
        transform: translate3d(0, 0, 0);
    }
    ul li:hover a,
    ul li:focus a {
        -webkit-transform: translateY(-100%);
        -moz-transform: translateY(-100%);
        transform: translateY(-100%);
    }
</style>
