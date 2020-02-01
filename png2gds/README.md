# PNG2GDS

This is a little compicated but it works well.

## Split the images

becase the png 2 gds process is pixel 2 pixel using cpu, it is very slow without multithreeding, so one
way is to split the iamges to X parts, then transfer them together,


you only need to run

```shell
bash split_results.sh
```

## run the transfer code

```shell
bash togds_split $sid
```

sid is the bash number, so tmux is recommender to open multi bash window at same time.

# However

This is not a perfect gds, the layer is croped into pixel level, we need use calibre's gds to oas tool to get the perfect oas or gds file.

Why not directly use calibre? Because calibre doesnot support the png input format.

The file is in the calibre gds2oas folder.
