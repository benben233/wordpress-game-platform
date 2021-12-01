<li class="alm-item<?php if (!has_post_thumbnail()) { ?> no-img<?php } ?>">
    <a href="<?php the_permalink(); ?>" title="<?php the_title(); ?>">
        <?php if (has_post_thumbnail()) {
            the_post_thumbnail();
        } ?>
        <h3><?php the_title(); ?></h3>
        <p class="entry-meta"><?php the_time("F d, Y"); ?></p>
    </a>
    <?php get_post_meta();  the_excerpt(); ?>
</li>
$custom = get_post_custom();
foreach($custom as $key => $value) {
     echo $key.': '.$value.'<br />';
}
<br><br>