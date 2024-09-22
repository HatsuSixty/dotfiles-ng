local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", -- latest stable release
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    "andweeb/presence.nvim",
    "sainnhe/sonokai",
    "folke/tokyonight.nvim",
    "ellisonleao/gruvbox.nvim",
    {
        'windwp/nvim-autopairs',
        event = "InsertEnter",
        opts = {}
    },
    "nvim-tree/nvim-web-devicons",
    "nvim-tree/nvim-tree.lua",
    "nvim-lualine/lualine.nvim",
    { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
    {
        "nvim-telescope/telescope.nvim",
        dependencies = { 'nvim-lua/plenary.nvim' }
    },
    {
        'VonHeikemen/lsp-zero.nvim',
        branch = 'v4.x',
        dependencies = {
            { 'neovim/nvim-lspconfig' },
            { 'williamboman/mason.nvim' },
            { 'williamboman/mason-lspconfig.nvim' },
            { 'hrsh7th/nvim-cmp' },
            { 'hrsh7th/cmp-nvim-lsp' },
            { 'L3MON4D3/LuaSnip' }
        }
    }
})
