#!/bin/bash

for position in rb wr te qb; do
  python -m randomize_player_urls $position
done