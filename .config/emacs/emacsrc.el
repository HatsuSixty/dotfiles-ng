;; make emacs stop asking about themes

(setq custom-safe-themes t)

;; simplify GUI & appearance

(menu-bar-mode 0)
(tool-bar-mode 0)
(scroll-bar-mode 0)
(column-number-mode 1)
(show-paren-mode 1)
(setq display-line-numbers-type 'relative)
(setq inhibit-startup-screen t)

(when (version<= "26.0.50" emacs-version)
  (global-display-line-numbers-mode))

(add-to-list 'default-frame-alist '(font . "FuraMono Nerd Font Mono 14"))

;; packages

(setq package-list '(multiple-cursors
                     company
                     gdscript-mode
                     yasnippet-snippets
                     yasnippet
                     yaml-mode
                     gruber-darker-theme
                     nasm-mode
                     rust-mode
                     magit
                     markdown-mode
                     lua-mode
                     csharp-mode
                     go-mode
                     rainbow-mode
                     doom-themes
                     astyle
                     whitespace-cleanup-mode
                     elcord
                     cmake-mode
                     ))

(setq package-archives '(("gnu" . "http://elpa.gnu.org/packages/")
                         ("melpa" . "http://melpa.org/packages/")))
(package-initialize)

(unless package-archive-contents
  (package-refresh-contents))

(dolist (package package-list)
  (unless (package-installed-p package)
    (package-install package)))

;; elcord

(elcord-mode)

;; autoload files

(mapc 'load (file-expand-wildcards "~/.config/emacs/lisp/*.el"))

;; setup themes

(add-to-list 'custom-theme-load-path "~/.config/emacs/themes/")

;;; tabs and spaces

(setq-default tab-width 4)
(setq-default indent-tabs-mode nil)

;;; c-mode

;;(add-to-list 'auto-mode-alist '("\\.[hc]\\(pp\\)?\\'" . simpc-mode))

(add-hook 'c-mode-hook (lambda ()
                         (interactive)
                         (c-toggle-comment-style -1)))

(setq-default c-basic-offset 4
              c-default-style '((java-mode . "java")
                                (awk-mode . "awk")
                                (other . "bsd")))

(add-hook 'simpc-mode-hook
          (lambda ()
            (interactive)
            (setq-local fill-paragraph-function 'astyle-buffer)
            (local-set-key (kbd "C-c C-f") 'astyle-region)))

;;; whitespace

(defconst USE-WHITESPACE 1)

(defun rc/set-up-whitespace-handling ()
  (interactive)
  (when (= USE-WHITESPACE 1) (whitespace-mode 1))
  (whitespace-cleanup-mode))

(add-hook 'tuareg-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'java-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'c-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'c++-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'lua-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'rust-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'scala-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'markdown-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'haskell-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'python-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'erlang-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'asm-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'nasm-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'go-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'nim-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'yaml-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'porth-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'north-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'no-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'loisp-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'simpc-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'gdscript-mode-hook 'rc/set-up-whitespace-handling)
(add-hook 'js-mode-hook 'rc/set-up-whitespace-handling)

(setq whitespace-style
   (quote
    (face tabs spaces trailing space-before-tab newline indentation empty space-after-tab space-mark tab-mark)))

;; yasnippets

(yas-global-mode 1)

;; multiple cursors

(global-set-key (kbd "C-x RET RET") 'mc/edit-lines)
(global-set-key (kbd "C->") 'mc/mark-next-like-this)
(global-set-key (kbd "C-<") 'mc/mark-previous-like-this)
(global-set-key (kbd "C-c C-<") 'mc/mark-all-like-this)

;; company mode

(global-company-mode)

(add-hook 'tuareg-mode-hook
          (lambda ()
            (interactive)
            (company-mode 0)))

;; duplicate line

(defun duplicate-line()
  (interactive)
  (move-beginning-of-line 1)
  (kill-line)
  (yank)
  (open-line 1)
  (next-line 1)
  (yank)
)

(global-set-key (kbd "C-d") 'duplicate-line)

;; nasm mode

(add-to-list 'auto-mode-alist '("\\.asm?\\'" . nasm-mode))
