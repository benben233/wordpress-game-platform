<li class="alm-item<?php if (!has_post_thumbnail()) { ?> no-img<?php } ?>">
    <a href="<?php the_permalink(); ?>" title="<?php the_title(); ?>">
        <?php if (has_post_thumbnail()) {
            the_post_thumbnail();
        } ?>
        <h3><?php the_title(); ?></h3>
        <p class="entry-meta"><?php the_time("F d, Y"); ?></p>
    </a>
    <?php get_post_meta();
    the_excerpt(); ?>
</li>

<?php
$custom = get_post_custom();
printf('%.2f%% of reviews for this game are positive <br>', 100 * $custom['reviews'][0]);
echo 'About ' . number_format($custom['owners'][0]) . ' people have this game<br>';
echo 'Developer: ' . $custom['developer'][0] . '<br>';
echo get_the_excerpt();
?>

<section class="skrollable u-align-center u-clearfix u-image u-lightbox u-parallax u-section-1" id="sec-b0c5" data-image-width="1438" data-image-height="810" style="background-image: url('<?php echo get_template_directory_uri(); ?>/images/media/<?php echo get_post_custom_values('appid')[0]; ?>/background.jpg'); background-color: #293b53;color: white;">
</section>
<?php
function my_games($args, $id)
{
    $args['meta_query'] = [
        'reviews' => [
            'key'     => 'reviews',
            'type'    => 'numeric',
        ],
        'owners' =>  [
            'key'     =>  'owners',
            'type'    => 'numeric'
        ]
    ];
}
?>