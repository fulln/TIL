## vim 安装fzf

### 简介
Fuzzy finder 是一款使用 GO 语言编写的交互式的 Unix 命令行工具。可以用来查找任何 列表 内容，文件、Git 分支、进程等。所有的命令行工具可以生成列表输出的都可以再通过管道 pipe 到 fzf 上进行搜索和查找

### 安装

在macos下 
```
brew install fzf
```

### 安装插件

如果你本地安装过 fzf 命令行工具了，只需要在 .vimrc 里面添加下面两个插件配置即可

```
Plug '/usr/local/opt/fzf'
Plug 'junegunn/fzf.vim'
```

### 自定义插件配置

我是参考的[这个](https://github.com/wsgggws/my-neovim-configurations)的配置

```
" ------------------------------------------------
"  For fzf.vim
" ------------------------------------------------
"<Leader>f在当前目录搜索文件
nnoremap <silent> <Leader>f :Files<CR>
nnoremap <silent> <C-p> :Files<CR>
"<Leader>b切换Buffer中的文件
nnoremap <silent> <Leader>b :Buffers<CR>
nnoremap <silent> <Leader>rg :Rg<CR>
"<Leader>p在当前所有加载的Buffer中搜索包含目标词的所有行，:BLines只在当前Buffer中搜索
nnoremap <silent> <Leader>l :BLines<CR>
"<Leader>h在Vim打开的历史文件中搜索，相当于是在MRU中搜索，:History：命令历史查找
nnoremap <silent> <Leader>h :History<CR>
"调用Rg进行搜索，包含隐藏文件
command! -bang -nargs=* Rg
  \ call fzf#vim#grep(
  \   'rg --column --line-number --no-heading --color=always --smart-case '.shellescape(<q-args>), 1,
  \   fzf#vim#with_preview(), <bang>0)
let g:fzf_preview_window = 'right:50%'
"
```
> 注意,如果使用rb  先用'brew install rb'进行安装


