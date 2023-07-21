require("hatsu.remap")
require("hatsu.packer")
require("hatsu.set")

local nvimrc = os.getenv("HOME") .. "/.config/nvim"

vim.cmd('source ' .. nvimrc .. '/lua/hatsu/darrows.vim')
