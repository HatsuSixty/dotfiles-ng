vim.g.mapleader = " "

vim.keymap.set("n", "<C-e>", function() vim.cmd[[NvimTreeOpen]] end)
vim.keymap.set("n", "<C-i>", function() vim.cmd[[NvimTreeClose]] end)
