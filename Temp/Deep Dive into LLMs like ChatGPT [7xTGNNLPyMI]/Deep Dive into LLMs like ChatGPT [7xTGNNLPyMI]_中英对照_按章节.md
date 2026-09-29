# Deep Dive into LLMs like ChatGPT｜中英对照（按章节）

> 来源：https://www.youtube.com/watch?v=7xTGNNLPyMI ｜ YouTube 自动字幕整理，仅滚动去重与分段，未做总结改写。英文为语音识别原稿，中文为机器翻译。注意：YouTube 提供的简体中文轨止于约 3:03:50（第 19 章 RLHF 中段），此后约 27 分钟仅有英文。

## 1. introduction（0:00:00–0:01:00）

### 0:00:02–0:00:23

EN：hi everyone so I've wanted to make this video for a while it is a comprehensive but General audience introduction to large language models like Chachi PT and what I'm hoping to achieve in this video is to give you kind of mental models for thinking through what it is that this tool is it is obviously magical and amazing in some respects it's uh really good at some things not very good at

中文：大家好，我一直想做这个 视频一段时间以来都很全面 但面向大众的介绍 大型语言模型，例如 Chachi PT 和 我希望通过这段视频达到的目标 目的是给你提供一些心理模型。 仔细思考这究竟是什么 这工具显然很神奇， 在某些方面，这真是令人惊叹。 擅长某些事情，但不擅长其他事情

### 0:00:23–0:00:42

EN：other things and there's also a lot of sharp edges to be aware of so what is behind this text box you can put anything in there and press enter but uh what should we be putting there and what are these words generated back how does this work and what what are you talking to exactly so I'm hoping to get at all those topics in this video we're going

中文：还有其他事情，还有很多 需要注意的锋利边缘是什么？ 在这个文本框后面，你可以放置 里面放任何东西，然后按回车键，但是呃…… 我们应该在那里放些什么？ 这些词是如何生成的？ 这项工作，还有你在说什么？ 正是如此，我希望能够完全理解。 本视频中我们将探讨的话题

### 0:00:42–0:01:04

EN：to go through the entire pipeline of how this stuff is built but I'm going to keep everything uh sort of accessible to a general audience so let's take a look at first how you build something like chpt and along the way I'm going to talk about um you know some of the sort of cognitive psychological implications of the tools okay so let's build Chachi PT so there's going to be multiple stages

中文：走完整个流程，看看如何 这些东西已经建好了，但我还要…… 保持所有东西都易于获取 面向普通大众，我们来看一看。 首先，你如何构建类似的东西？ 在这一章里，我会边讲边说 关于……你知道，某种程度上…… 认知心理学意义 工具都准备好了，那我们来搭建 Chachi PT 吧。 所以会分多个阶段进行。

## 2. pretraining data (internet)（0:01:00–0:07:47）

### 0:01:04–0:01:28

EN：arranged sequentially the first stage is called the pre-training stage and the first step of the pre-training stage is to download and process the internet now to get a sense of what this roughly looks like I recommend looking at this URL here so um this company called hugging face uh collected and created and curated this data set called Fine web and they go into a lot of detail on

中文：按顺序排列的第一阶段是 称为预备训练阶段和 预训练阶段的第一步是 现在下载和处理互联网 为了大致了解这是什么意思 看来我建议看看这个 网址在这里，所以嗯，这家公司叫 拥抱脸呃收集和创造 并整理了名为 Fine 的数据集。 网站上有很多关于这方面的详细信息。

### 0:01:28–0:01:50

EN：this block post on how how they constructed the fine web data set and all of the major llm providers like open AI anthropic and Google and so on will have some equivalent internally of something like the fine web data set so roughly what are we trying to achieve here we're trying to get ton of text from the internet from publicly available sources so we're trying to have a huge quantity of very high

中文：这篇帖子是关于他们如何运作的 构建了精细的网络数据集， 所有主要的LLM提供商，例如Open，都提供LLM服务。 AI anthropic 和谷歌等等将会 内部有一些等效的东西 类似精细网络数据集之类的东西 我们大致想要达到什么目标 我们在这里试图获取大量文本 来自互联网，公开 我们正在努力利用现有资源。 拥有大量非常高的

### 0:01:50–0:02:11

EN：quality documents and we also want very large diversity of documents because we want to have a lot of knowledge inside these models so we want large diversity of high quality documents and we want many many of them and achieving this is uh quite complicated and as you can see here takes multiple stages to do well so let's take a look at what some of these stages look like in a bit for now I'd

中文：高质量的文件，我们也希望非常 因为我们拥有种类繁多的文件，所以 想掌握很多知识 因此，我们希望这些模型具有高度多样性。 我们需要高质量的文件。 其中很多很多，而实现这一点是 嗯，相当复杂，正如你所看到的。 要做好这件事，需要经历多个阶段。 让我们来看看其中一些是什么。 阶段看起来好像过一会儿就会开始了，目前我……

### 0:02:11–0:02:31

EN：like to just like to note that for example the fine web data set which is fairly representative what you would see in a production grade application actually ends up being only about 44 terabyt of dis space um you can get a USB stick for like a terabyte very easily or I think this could fit on a single hard drive almost today so this is not a huge amount of data at the end

中文：我想指出的是，对于 例如，精细网络数据集是 相当具有代表性，你会看到 在生产级应用中 实际上最终只有大约44个 太字节的这个空间，嗯，你可以得到一个 一个容量高达1TB的U盘 很容易，或者我觉得这可以放在一个 今天几乎只剩下一块硬盘了，所以这 最后的数据量并不大。

### 0:02:31–0:02:52

EN：of the day even though the internet is very very large we're working with text and we're also filtering it aggressively so we end up with about 44 terabytes in this example so let's take a look at uh kind of what this data looks like and what some of these stages uh also are so the starting point for a lot of these efforts and something that contributes most of the data by the end of it is

中文：即使互联网是当今时代的产物， 非常非常大，我们正在处理文本 而且我们还在积极进行过滤。 所以最终我们得到了大约 44 TB 的数据。 这个例子，我们来看一下…… 这些数据大概长什么样？ 这些阶段中有些也如此 很多这类事情的起点 努力和贡献 到最后，大部分数据是

### 0:02:52–0:03:14

EN：Data from common crawl so common craw is an organization that has been basically scouring the internet since 2007 so as of 2024 for example common CW has indexed 2.7 billion web pages uh and uh they have all these crawlers going around the internet and what you end up doing basically is you start with a few seed web pages and then you follow all the links and you just

中文：来自常用爬虫的数据，所以常用爬虫是 一个基本上 自 2007 年以来一直在互联网上搜索，以便 例如，2024 年常见的 CW 有 索引了 27 亿个网页 页面，呃，它们都有这些 爬虫程序在互联网上四处运行 你最终所做的基本上就是你 先从几个种子网页开始，然后 你点击所有链接，然后你就会……

### 0:03:15–0:03:35

EN：keep following links and you keep indexing all the information and you end up with a ton of data of the internet over time so this is usually the starting point for a lot of the uh for a lot of these efforts now this common C data is quite raw and is filtered in many many different ways so here they Pro they document this is the same diagram they document a little

中文：继续关注这些链接，你就会一直 索引所有信息，然后你就结束了。 收集了大量互联网数据 随着时间的推移，这通常是 很多事情的起点都是…… 现在很多这样的努力都与这个共同的C有关 数据较为原始，并且经过了过滤。 很多很多不同的方式 所以在这里，他们记录了这一点。 他们记录的同一张图表略有不同。

### 0:03:35–0:03:47

EN：bit the kind of processing that happens in these stages so the first thing here is something called URL filtering so what that is referring to is that there's these block

中文：但这种处理方式确实会发生。 在这些阶段中，首先要做的事情是…… 它叫做URL。 过滤指的是什么？ 就是这些块

### 0:03:50–0:04:10

EN：lists of uh basically URLs that are or domains that uh you don't want to be getting data from so usually this includes things like U malware websites spam websites marketing websites uh racist websites adult sites and things like that so there's a ton of different types of websites that are just eliminated at this stage because we don't want them in our data set um the second part is text extraction you have

中文：基本上是 URL 列表，或者 你不想成为的域名 通常情况下，从这里获取数据 包括诸如恶意软件网站之类的东西 垃圾邮件网站 营销网站 呃 种族主义网站、成人网站等等 像这样，所以有很多不同的 仅此类型的网站 因为我们在此阶段被淘汰，所以 我们不希望它们出现在我们的数据集中。 第二部分是文本提取，您有

### 0:04:10–0:04:33

EN：to remember that all these web pages this is the raw HTML of these web pages that are being saved by these crawlers so when I go to inspect here this is what the raw HTML actually looks like you'll notice that it's got all this markup uh like lists and stuff like that and there's CSS and all this kind of stuff so this is um computer code almost for these web pages but what

中文：记住所有这些网页 这是这些网页的原始HTML代码 这些爬行动物正在拯救它们 所以当我去检查的时候 这就是原始 HTML 的实际内容。 看起来你会注意到它有 所有这些标记，比如列表之类的东西 就是这样，还有CSS等等。 诸如此类的东西，所以这是……电脑 这些网页几乎都用了代码，但是……

### 0:04:33–0:04:56

EN：we really want is we just want this text right we just want the text of this web page and we don't want the navigation and things like that so there's a lot of filtering and processing uh and heris that go into uh adequately filtering for just their uh good content of these web pages the next stage here is language filtering so for example fine web filters uh using a language classifier

中文：我们真正想要的，就是这段文字。 没错，我们只需要这个网页的文本。 页面，我们不需要导航。 诸如此类的事情有很多。 过滤和处理 uh 和 heris 这就需要进行充分的过滤了。 他们网站上的内容确实不错。 页面，下一阶段是语言 过滤，例如精细网络 使用语言分类器过滤呃

### 0:04:56–0:05:15

EN：they try to guess what language every single web page is in and then they only keep web pages that have more than 65% of English as an example and so you can get a sense that this is like a design decision that different companies can uh can uh take for themselves what fraction of all different types of languages are we going to include in our data set because

中文：他们试图猜测每种语言是什么 单个网页已插入，然后他们就只有 保留浏览量超过 65% 的网页 英语作为一种 例如，这样你就能明白…… 这就像一个设计决策， 不同的公司可以……可以……拿走 他们自己能从中获得多少？ 我们有不同类型的语言。 因为要将其纳入我们的数据集，所以

### 0:05:15–0:05:34

EN：for example if we filter out all of the Spanish as an example then you might imagine that our model later will not be very good at Spanish because it's just never seen that much data of that language and so different companies can focus on multilingual performance to uh to a different degree as an example so fine web is quite focused on English and so their language model if they end up

中文：例如，如果我们过滤掉所有的 以西班牙语为例，那么你可能会…… 想象一下，我们后来的模型将不再是 我西班牙语很好，因为它就是 从未见过这么多相关数据。 语言，因此不同的公司可以 专注于多语言表演 例如，程度有所不同。 fine web 非常注重英语， 所以，如果他们最终采用的是他们的语言模型的话

### 0:05:35–0:05:58

EN：training one later will be very good at English but not may be very good at other languages after language filtering there's a few other filtering steps and D duplication and things like that um finishing with for example the pii removal this is personally identifiable information so as an example addresses Social Security numbers and things like that you would try to detect them and you would try to filter out those kinds

中文：稍后训练一个会非常有效 英语可能不太好 其他 语言过滤后的语言 还有一些其他的筛选步骤， D 重复之类的东西 最后以pii为例 删除此信息涉及个人身份信息 例如地址等信息 社会安全号码等等 你会尝试去发现它们，并且 你会尝试过滤掉那些类型的

### 0:05:58–0:06:16

EN：of web pages from the the data set as well so there's a lot of stages here and I won't go into full detail but it is a fairly extensive part of the pre-processing and you end up with for example the fine web data set so when you click in on it uh you can see some examples here of what this actually ends up looking like and anyone can download

中文：从数据集中提取网页 这里有很多阶段， 我不会详述细节，但确实如此。 相当大一部分 预处理后，最终得到： 例如，精细的网络数据集，所以当 你点击进去，就能看到一些 以下是一些实际结局的例子。 看起来像这样，任何人都可以下载

### 0:06:16–0:06:43

EN：this on the huging phase web page and so here are some examples of the final text that ends up in the training set so this is some article about tornadoes in 2012 um so there's some t tadoes in 2020 in 2012 and what happened uh this next one is something about did you know you have two little yellow 9vt battery sized adrenal glands in your body okay so this is some kind

中文：这是在拥抱阶段网页上看到的，等等。 以下是一些最终文本的示例。 最终它会被纳入训练集，所以这样 这是一篇关于龙卷风的文章 2012年，嗯，所以2020年有一些t tadoes 2012年以及什么 发生了什么事？呃，接下来这个有点奇怪。 你知道你有两个孩子吗？ 黄色9伏电池大小的肾上腺 在你的身体里，好吧，这是某种

### 0:06:43–0:07:06

EN：of a odd medical article so just think of these as basically uh web pages on the internet filtered just for the text in various ways and now we have a ton of text 40 terabytes off it and that now is the starting point for the next step of this stage now I wanted to give you an intuitive sense of where we are right now so I took the first 200 web pages

中文：奇怪的医疗 文章内容，所以就把这些看作是 基本上就是互联网上的网页 仅筛选各种文本 方式很多，现在我们有很多文本 40 从中剥离了TB级的数据，现在就是这样了。 这是下一步的起点。 现在我想给你一个舞台 直觉告诉我们，我们正处于正确的位置。 所以我选取了前200个网页

### 0:07:06–0:07:28

EN：here and remember we have tons of them and I just take all that text and I just put it all together concatenate it and so this is what we end up with we just get this just just raw text raw internet text and there's a ton of it even in these 200 web pages so I can continue zooming out here and we just have this like massive tapestry of Text data and

中文：这里有很多，记住我们有很多。 我就把所有这些文字都拿过来，然后我就 把它们全部组合起来，连接起来，然后 所以这就是我们最终得到的结果。 获取这些原始文本，来自互联网 文本，而且数量很多，甚至在…… 这200个网页，这样我才能继续。 镜头拉远，我们就能看到这些。 就像一幅巨大的文本数据挂毯

### 0:07:28–0:07:52

EN：this text data has all these p patterns and what we want to do now is we want to start training neural networks on this data so the neural networks can internalize and model how this text flows right so we just have this giant texture of text and now we want to get neural Nets that mimic it okay now before we plug text into neural networks we have to decide how we're going to

中文：这段文本数据包含了所有这些p模式 而我们现在想做的是，我们想…… 开始在此基础上训练神经网络 数据，以便神经网络可以 理解并模仿这段文字 流程很顺畅，所以我们就有了这个巨大的 文本的纹理，现在我们想要获取 模仿它的神经网络现在可以了。 在我们将文本输入神经网络之前 我们必须决定我们将如何……

## 3. tokenization（0:07:47–0:14:27）

### 0:07:52–0:08:16

EN：represent this text uh and how we're going to feed it in now the way our technology works for these neuron Lots is that they expect a one-dimensional sequence of symbols and they want a finite set of symbols that are possible and so we have to decide what are the symbols and then we have to represent our data as one-dimensional sequence of those symbols so right now what we have is a

中文：代表这段文字，以及我们是如何…… 现在就按我们的方式喂它 科技对这些神经元来说非常有效。 他们期望 一维符号序列 他们想要的是一组有限的符号。 这些都是有可能的，所以我们必须 确定符号是什么，然后我们 必须将我们的数据表示为 那些一维序列 符号，所以现在我们有的是

### 0:08:16–0:08:38

EN：onedimensional sequence of text it starts here and it goes here and then it comes here Etc so this is a onedimensional sequence even though on my monitor of course it's laid out in a two-dimensional way but it goes from left to right and top to bottom right so it's a one-dimensional sequence of text now this being computers of course there's an underlying representation here so if I do what's called utf8 uh

中文：一维文本序列 从这里开始，到这里结束，然后它 来到这里等等，所以这是一个 即使是一维序列 我的显示器当然是摆放在…… 二维方式，但它从 从左到右，从上到下，所以 它是一维的文本序列。 当然，这里指的是计算机。 这里存在一种潜在的表征 所以，如果我使用所谓的utf8编码，呃……

### 0:08:38–0:09:04

EN：encode this text then I can get the raw bits that correspond to this text in the computer and that's what uh that looks like this so it turns out that for example this very first bar here is the first uh eight bits as an example so what is this thing right this is um representation that we are looking for uh in in a certain sense we have

中文：对这段文本进行编码后，我就可以得到原始文本了。 与此文本对应的部分 电脑，那就是它的样子。 像这样，结果发现对于 例如，这里的第一个小节就是 前八个比特作为 举个例子，那么这个东西到底是什么呢？ 嗯，这就是我们正在寻找的代表。 嗯，从某种意义上说，我们有

### 0:09:04–0:09:32

EN：exactly two possible symbols zero and one and we have a very long sequence of it right now as it turns out um this sequence length is actually going to be very finite and precious resource uh in our neural network and we actually don't want extremely long sequences of just two symbols instead what we want is we want to trade off uh this um symbol size uh of this vocabulary as we call it

中文：恰好有两个可能的符号：零和 一，我们有一个很长的序列 现在看来，嗯，就是这样 序列长度实际上将是 非常有限且珍贵的资源 我们的神经网络，但我们实际上并没有 想要非常长的序列 我们想要的是两个符号，而不是两个符号。 想交易这个符号 我们称之为这种词汇的大小

### 0:09:32–0:10:00

EN：and the resulting sequence length so we don't want just two symbols and extremely long sequences we're going to want more symbols and shorter sequences okay so one naive way of compressing or decreasing the length of our sequence here is to basically uh consider some group of consecutive bits for example eight bits and group them into a single what's called bite so because uh these bits are either on or off if we take a

中文：以及由此产生的序列长度，因此我们 不只是两个符号而已 我们将要处理的序列非常长 想要更多符号和更短的序列 好的，所以一种简单的压缩方法或 缩短序列的长度 这里基本上是要考虑一些事情 例如一组连续的比特 八位二进制数，并将它们组合成一个单一的二进制数。 之所以称之为咬伤，是因为……这些 如果我们取一个数据点，那么这些位要么是开的，要么是关的。

### 0:10:00–0:10:22

EN：group of eight of them there turns out to be only 256 possible combinations of how these bits could be on or off and so therefore we can re repesent this sequence into a sequence of bytes instead so this sequence of bytes will be eight times shorter but now we have 256 possible symbols so every number here goes from 0 to 255 now I really encourage you to think

中文：结果发现他们一共八个人。 只有 256 种可能的组合 这些部件如何才能打开或关闭等等 因此我们可以重新表示这一点。 将序列转换为字节序列 因此，这一系列字节将 原本会短八倍，但现在我们有 256 个可能的符号，所以每个数字 这里从 0 到 255 现在我真的鼓励你们思考

### 0:10:22–0:10:46

EN：of these not as numbers but as unique IDs or like unique symbols so maybe it's a bit more maybe it's better to actually think of these to replace every one of these with a unique Emoji you'd get something like this so um we basically have a sequence of emojis and there's 256 possible emojis you can think of it that way now it turns out that in production for state-of-the-art language

中文：这些并非作为数字，而是作为唯一实体。 ID 或类似的唯一符号，所以也许是这样 或许再多一点，实际上会更好。 想想这些可以替换掉每一个 这些带有独特表情符号的表情符号会给你带来什么好处？ 大概就是这样，所以，我们基本上 有一系列表情符号，然后…… 你能想到的256种表情符号 这样看来，现在看来，在 最先进语言的生产

### 0:10:46–0:11:10

EN：models uh you actually want to go even Beyond this you want to continue to shrink the length of the sequence uh because again it is a precious resource in return for more symbols in your vocabulary and the way this is done is done by running what's called The Bite pair encoding algorithm and the way this works is we're basically looking for consecutive bytes or symbols that are

中文：模型，呃，你实际上想更进一步。 除此之外，你还想继续 缩短序列的长度 因为它是一种宝贵的资源。 作为回报，您将获得更多符号 词汇以及实现方式是 通过运行名为“The Bite”的程序来实现。 配对编码算法及其实现方式 作品就是我们基本上在寻找的东西 连续的字节或符号

### 0:11:10–0:11:34

EN：very common so for example turns out that the sequence 116 followed by 32 is quite common and occurs very frequently so what we're going to do is we're going to group uh this um pair into a new symbol so we're going to Mint a symbol with an ID 256 and we're going to rewrite every single uh pair 11632 with this new symbol and then can we can

中文：非常常见，例如结果证明 序列 116 后跟 32 是 很常见，而且发生频率很高。 所以我们接下来要做的事就是…… 将这对组合成一个新的 符号，所以我们要铸造一个符号 ID 为 256，我们将要 用以下方式重写每一对 11632 这个新符号，然后我们就可以……

### 0:11:34–0:12:04

EN：iterate this algorithm as many times as we wish and each time when we mint a new symbol we're decreasing the length and we're increasing the symbol size and in practice it turns out that a pretty good setting of um the basically the vocabulary size turns out to be about 100,000 possible symbols so in particular GPT 4 uses 100, 277 symbols um and this process of converting from

中文：将此算法迭代多次 我们希望，每次我们铸造新的 我们正在缩短符号的长度， 我们正在增大符号尺寸，并且在 实践证明，这相当不错 基本上是这样的 词汇量大约是 所以有 100,000 个可能的符号 特定的 GPT 4 用途 100， 277 个符号 嗯，以及从……转换的过程

### 0:12:04–0:12:29

EN：raw text into these symbols or as we call them tokens is the process called tokenization so let's now take a look at how gp4 performs tokenization conting from text to tokens and from tokens back to text and what this actually looks like so one website I like to use to explore these token representations is called tick tokenizer and so come here to the drop down and select CL 100 a

中文：将原始文本转换成这些符号，或者正如我们 将它们称为令牌的过程称为 标记化，现在让我们来看一下…… gp4 如何执行分词 从文本到词元，以及从词元到文本的转换 文本以及它实际看起来的样子 比如我喜欢用的某个网站 探索这些标记表示是 它被称为 tick tokenizer，所以来到这里 在下拉菜单中选择 CL 100 a

### 0:12:29–0:13:02

EN：base which is the gp4 base model tokenizer and here on the left you can put in text and it shows you the tokenization of that text so for example heo space world so hello world turns out to be exactly two Tokens The Token hello which is the token with ID 15339 and the token space world that is the token 1 1917 so um hello space world now if I

中文：基础型，即GP4基础模型 分词器，在左侧您可以…… 输入文本，它会显示出来 对该文本进行分词，例如 赫奥空间 世界，所以你好世界，结果发现是 恰好有两个令牌，令牌是 hello，哪个 是 ID 为 的令牌 15339 和代币空间 这是令牌 1 的世界 1917年，嗯，你好，太空世界，现在如果我

### 0:13:02–0:13:26

EN：was to join these two for example I'm going to get again two tokens but it's the token H followed by the token L world without the H um if I put in two Spa two spaces here between hello and world it's again a different uh tokenization there's a new token 220 here okay so you can play with this and see what happens here also keep in mind

中文：例如，将这两个人结合起来，我是 我还会再获得两个代币，但是…… 标记 H 后跟标记 L 没有世界 嗯，如果我在这里放两个 Spa 两个空格的话 在“你好”和“世界”之间，又是一个 不同的分词方法，有一种新的 令牌 220 好了，你可以玩玩这个。 看看这里会发生什么，还要记住……

### 0:13:26–0:13:50

EN：this is not uh this is case sensitive so if this is a capital H it is something else or if it's uh hello world then actually this ends up being three tokens instead of just two tokens yeah so you can play with this and get an sort of like an intuitive sense of uh what these tokens work like we're actually going to loop around to tokenization a bit later in the video

中文：这不是……呃……这是区分大小写的，所以 如果这是大写的 H，那它就代表某种东西。 否则，或者如果它是“你好，世界”之类的程序…… 实际上，这最终会得到三个代币。 而不是只有两个 是的，代币，所以你可以用这个玩。 并获得一种类似直觉的感觉 大概了解这些代币的工作原理 我们实际上要绕回…… 视频稍后会用到分词。

### 0:13:50–0:14:16

EN：for now I just wanted to show you the website and I wanted to uh show you that this text basically at the end of the day so for example if I take one line here this is what GT4 will see it as so this text will be a sequence of length 62 this is the sequence here and this is how the chunks of text correspond to these symbols and again there's 100,

中文：现在我只想给你们看看…… 网站，我想给你展示一下。 这段文字基本上位于结尾处 例如，如果我一天只取一行 这就是GT4会如何看待它的。 这段文本将是一段长度为的序列 62 这是这里的序列，这是 文本块如何对应 这些符号，而且又有100个，

### 0:14:16–0:14:40

EN：27777 possible symbols and we now have one-dimensional sequences of those symbols so um yeah we're going to come back to tokenization but that's uh for now where we are okay so what I've done now is I've taken this uh sequence of text that we have here in the data set and I have re-represented it using our tokenizer into a sequence of tokens and this is what that looks like now so for

中文：27777 个可能的符号，我们现在有 这些一维序列 符号，所以嗯，是的，我们要来了 回到分词的话题，但那是……呃…… 现在我们一切都好，所以我已经做了 现在我已经采取了这一步骤 我们数据集中的文本 我已使用我们的重新表示了它 将分词器分解成一系列标记， 这就是它现在的样子，所以……

## 4. neural network I/O（0:14:27–0:20:11）

### 0:14:40–0:15:01

EN：example when we go back to the Fine web data set they mentioned that not only is this 44 terab of dis space but this is about a 15 trillion token sequence of um in this data set and so here these are just some of the first uh one or two or three or a few thousand here I think uh tokens of this data set but there's 15

中文：例如，当我们回到 Fine 网站时 他们提到的数据集不仅如此 这44太拉的dis空间，但这却是 大约 15 万亿个 um 的代币序列 在这个数据集中，所以这里是 只是最初的一两个，或者 我想这里有三千或几千人吧。 该数据集包含 15 个标记。

### 0:15:01–0:15:22

EN：trillion here uh to keep in mind and again keep in mind one more time that all of these represent little text chunks they're all just like atoms of these sequences and the numbers here don't make any sense they're just uh they're just unique IDs okay so now we get to the fun part which is the uh neural network training and this is where a lot of the heavy lifting happens

中文：这里有一万亿需要记住。 再次提醒大家： 这些都代表少量文字。 它们就像原子一样，都是由许多块组成的。 这些序列和这里的数字 完全没道理，它们只是…… 它们只是唯一的ID，好的，所以现在我们 接下来就是有趣的部分了，呃…… 神经网络训练，这就是 很多繁重的工作都发生在这里。

### 0:15:23–0:15:51

EN：computationally when you're training these neural networks so what we do here in this this step is we want to model the statistical relationships of how these tokens follow each other in the sequence so what we do is we come into the data and we take Windows of tokens so we take a window of tokens uh from this data fairly randomly and um the windows length can range anywhere anywhere between uh zero

中文：在训练过程中进行计算 这些神经网络，所以我们在这里做什么呢？ 在这一步中，我们想要建模 统计关系如何 这些代币依次出现 顺序，所以我们所做的就是进入 数据，我们取令牌窗口 所以我们取一个令牌窗口 这些数据相当 随机地，嗯，窗口长度可以 范围在零到零之间的任何位置。

### 0:15:51–0:16:16

EN：tokens actually all the way up to some maximum size that we decide on uh so for example in practice you could see a token with Windows of say 8,000 tokens now in principle we can use arbitrary window lengths of tokens uh but uh processing very long uh basically U window sequences would just be very computationally expensive so we just kind of decide that say 8,000 is a good

中文：代币实际上一直到某些 我们决定的最大尺寸，嗯，所以对于 例如，在实践中你可以看到 令牌，例如 Windows 8,000 个令牌 原则上我们可以使用任意 标记的窗口长度，但是，呃 处理时间很长，基本上是 U 窗口序列会非常 计算成本太高，所以我们就…… 大致决定一下，比如说8000是个不错的数字。

### 0:16:16–0:16:45

EN：number or 4,000 or 16,000 and we crop it there now in this example I'm going to be uh taking the first four tokens just so everything fits nicely so these tokens we're going to take a window of four tokens this bar view in and space single which are these token IDs and now what we're trying to do here is we're trying to basically predict the token that comes next in the sequence so

中文：数字是 4,000 或 16,000，然后我们裁剪它。 现在在这个例子中，我将要 呃，先拿走前四个代币 所以一切都很合适，所以这些 代币 我们将采用四的窗口期。 此栏视图中的代币和空间单个 这些代币是什么？ ID，以及我们现在在这里要做的事情 我们基本上是在试图预测…… 序列中下一个标记

### 0:16:45–0:17:08

EN：3962 comes next right so what we do now here is that we call this the context these four tokens are context and they feed into a neural network and this is the input to the neural network now I'm going to go into the detail of what's inside this neural network in a little bit for now it's important to understand is the input and the output of the neural net so the input are

中文：接下来是 3962，对吧？那我们现在该怎么办？ 这里我们称之为语境。 这四个标记是上下文，它们 输入到神经系统 网络，这是网络的输入。 神经网络 现在我将详细介绍…… 这个神经网络内部究竟是什么？ 现在稍微做一点很重要 理解输入和输出 神经网络的输入是

### 0:17:08–0:17:39

EN：sequences of tokens of variable length anywhere between zero and some maximum size like 8,000 the output now is a prediction for what comes next so because our vocabulary has 100277 possible tokens the neural network is going to Output exactly that many numbers and all of those numbers correspond to the probability of that token as coming next in the sequence so it's making guesses about what comes next um in the beginning this neural

中文：长度可变的标记序列 介于零和某个最大值之间的任何值 大小类似 8,000，现在的输出是 对接下来会发生什么做出预测 因为我们的词汇量有 100277 个可能的标记 神经 网络将输出完全相同的内容。 许多数字 所有这些数字都对应于 该代币出现的概率 接下来是序列中的下一个步骤，所以它正在制作 猜测接下来会发生什么 接下来，嗯，在开始时这个神经元

### 0:17:39–0:18:01

EN：network is randomly initialized so um and we're going to see in a little bit what that means but it's a it's a it's a random transformation so these probabilities in the very beginning of the training are also going to be kind of random uh so here I have three examples but keep in mind that there's 100,000 numbers here um so the probability of this token space Direction neural network is saying that

中文：网络是随机初始化的，所以…… 我们一会儿就会看到了。 这意味着什么，但它是，它是，它是 随机变换，所以这些 概率在最初阶段 培训也会很友好 随机的，呃，所以这里有三个 举例说明，但请记住，这只是其中一部分。 这里有10万个数字，嗯，所以 该令牌空间的概率 方向神经网络表示：

### 0:18:01–0:18:28

EN：this is 4% likely right now 11799 is 2% and then here the probility of 3962 which is post is 3% now of course we've sampled this window from our data set so we know what comes next we know and that's the label we know that the correct answer is that 3962 actually comes next in the sequence so now what we have is this mathematical process for doing an update to the neural network we

中文：目前这种可能性为 4%，11799 的可能性为 2%。 然后这里是3962的概率 目前帖子占比为3%，当然我们已经 我们从数据集中采样了该窗口，因此 我们知道接下来会发生什么，我们知道。 那是我们知道的标签 正确答案是 3962 实际上 接下来是什么？ 我们所拥有的就是这个数学过程 我们正在对神经网络进行更新。

### 0:18:28–0:18:51

EN：have the way of tuning it and uh we're going to go into a little bit of of detail in a bit but basically we know that this probability here of 3% we want this probability to be higher and we want the probabilities of all the other tokens to be lower and so we have a way of mathematically calculating how to adjust and update the neural network so that

中文：有办法调整它，嗯，我们是 接下来我会稍微深入探讨一下…… 稍后会详细说明，但基本上我们知道 我们想要的这个概率是3%。 这种概率会更高，而且我们 想知道其他所有情况的概率 代币 降低，所以我们有办法 通过数学计算来调整 并更新神经网络，以便

### 0:18:51–0:19:14

EN：the correct answer has a slightly higher probability so if I do an update to the neural network now the next time I Fe this particular sequence of four tokens into neural network the neural network will be slightly adjusted now and it will say Okay post is maybe 4% and case now maybe is 1% and uh Direction could become 2% or something like that and so we have a way

中文：正确答案略高一些。 所以如果我对概率进行更新， 神经网络现在下次我 Fe 这四个标记的特定序列 进入神经网络 现在会稍作调整，而且 会说好的，帖子可能是 4%，而且情况如此。 现在也许是 1% 和 uh Direction 可能会变成 2% 或 诸如此类，所以我们有办法

### 0:19:14–0:19:38

EN：of nudging of slightly updating the neuronet to um basically give a higher probability to the correct token that comes next in the sequence and now you just have to remember that this process happens not just for uh this um token here where these four fed in and predicted this one this process happens at the same time for all of these tokens in the entire data set and so in

中文：略微调整更新 神经网络基本上能提供更高的 正确令牌的概率 接下来是序列中的下一个，现在轮到你了。 只需记住这个过程 这种情况并非只发生在这个代币上。 这里是这四个人进食的地方 预测了这一过程。 同时，对于所有这些代币 在整个数据集中，因此在

### 0:19:38–0:20:01

EN：practice we sample little windows little batches of Windows and then at every single one of these tokens we want to adjust our neural network so that the probability of that token becomes slightly higher and this all happens in parallel in large batches of these tokens and this is the process of training the neural network it's a sequence of updating it so that it's predictions match up the statistics of

中文：我们练习时会抽取一些小窗口的小样本 批量安装 Windows，然后在每个 我们想要的这些代币中的单个 调整我们的神经网络，以便 该代币的概率变为 略高一些，而这一切都发生在 并行处理大量此类产品 代币，这就是过程 训练神经网络是 更新顺序，使其成为 预测结果与统计数据相符

### 0:20:01–0:20:24

EN：what actually happens in your training set and its probabilities become consistent with the uh statistical patterns of how these tokens follow each other in the data so let's now briefly get into the internals of these neural networks just to give you a sense of what's inside so neural network internals so as I mentioned we have these inputs uh that are sequences of tokens in this case this is four input

中文：你的训练中实际发生了什么 集合及其概率变为 与统计学一致 这些标记如何跟随彼此的模式 数据中还有其他内容，所以我们现在简要地看一下。 深入了解这些神经元的内部结构 网络只是为了让你了解一下 神经网络内部是什么？ 内部结构正如我提到的，我们有 这些输入是序列 在这种情况下，令牌是四个输入。

## 5. neural network internals（0:20:11–0:26:01）

### 0:20:24–0:20:48

EN：tokens but this can be anywhere between zero up to let's say 8,000 tokens in principle this can be an infinite number of tokens we just uh it would just be too computationally expensive to process an infinite number of tokens so we just crop it at a certain length and that becomes the maximum context length of that uh model now these inputs X are mixed up in a giant mathematical expression together

中文：代币，但这可以是介于两者之间的任何位置 数量从零到比如说 8,000 个代币 原则上，这可以是无限多个。 代币方面，我们只是……嗯，它就只是…… 处理成本过高，计算量太大。 令牌数量无穷无尽，所以我们只需 将其修剪到一定长度。 成为最大上下文长度 那个呃 现在模型中这些输入 X 混杂在一起 一个巨大的数学表达式

### 0:20:48–0:21:16

EN：with the parameters or the weights of these neural networks so here I'm showing six example parameters and their setting but in practice these uh um modern neural networks will have billions of these uh parameters and in the beginning these parameters are completely randomly set now with a random setting of parameters you might expect that this uh this neural network would make random predictions and it does in the beginning it's totally

中文：参数或权重 这些神经网络，所以我在这里 展示六个示例参数及其 设置，但实际上这些呃…… 现代神经网络将拥有 数十亿个这样的参数，而且 这些参数的起始点是 现在完全随机设置 随机设置参数可能会 预计这个神经网络 会做出随机预测，而且 一开始确实如此

### 0:21:16–0:21:42

EN：random predictions but it's through this process of iteratively updating the network uh as and we call that process training a neural network so uh that the setting of these parameters gets adjusted such that the outputs of our neural network becomes consistent with the patterns seen in our training set so think of these parameters as kind of like knobs on a DJ set and as you're twiddling these knobs you're getting

中文：随机预测，但正是通过这种方式。 迭代更新过程 网络呃，我们称之为过程 训练神经网络，所以…… 设置这些参数会得到 调整后，我们的输出结果 神经网络变得与……一致 我们在训练中观察到的模式 设置，所以把这些参数看作是某种类型 就像DJ台上的旋钮一样，当你…… 摆弄这些旋钮，你会得到

### 0:21:42–0:22:08

EN：different uh predictions for every possible uh token sequence input and training in neural network just means discovering a setting of parameters that seems to be consistent with the statistics of the training set now let me just give you an example what this giant mathematical expression looks like just to give you a sense and modern networks are massive expressions with trillions of terms probably but let me just show you a simple example here

中文：针对每件事的不同预测 可能的 uh 标记序列输入和 神经网络训练仅仅意味着 发现一组参数 似乎与此一致 训练统计数据 现在，我给你举个例子。 这个巨大的数学表达式是什么？ 看起来只是为了让你有个感觉而已。 现代网络是庞大的表达形式 可能有数万亿个词条，但还是…… 我这里给你举个简单的例子。

### 0:22:08–0:22:33

EN：it would look something like this I mean these are the kinds of Expressions just to show you that it's not very scary we have inputs x uh like X1 x2 in this case two example inputs and they get mixed up with the weights of the network w0 W1 2 3 Etc and this mixing is simple things like multiplication addition addition exponentiation division Etc and it is the subject of neural network

中文：我的意思是，它看起来大概是这样的。 这些就是表达式的类型。 为了向你证明它并没有那么可怕，我们 输入 x 例如本例中的 X1 和 X2 两个示例输入，结果混淆了。 网络权重为 w0 W1 2 3 等等，这种混合很简单。 就像乘法加法一样 指数运算、除法等等，它是 神经网络的主题

### 0:22:34–0:23:01

EN：architecture research to design effective mathematical Expressions uh that have a lot of uh kind of convenient characteristics they are expressive they're optimizable they're paralyzable Etc and so but uh at the end of the day these are these are not complex expressions and basically they mix up the inputs with the parameters to make predictions and we're optimizing uh the parameters of this neural network so that the predictions come out consistent

中文：建筑研究设计 有效的数学表达式 有很多方便之处 它们具有表现力的特征 它们既可优化，又可瘫痪。 等等等等，但归根结底…… 这些并不复杂。 表达方式，基本上都是混杂在一起的。 输入参数以进行制作 预测，我们正在优化…… 该神经网络的参数如下 预测结果与实际情况相符。

### 0:23:01–0:23:24

EN：with the training set now I would like to show you an actual production grade example of what these neural networks look like so for that I encourage you to go to this website that has a very nice visualization of one of these networks so this is what you will find on this website and this neural network here that is used in production settings has this special kind of structure this

中文：现在有了训练集，我希望 向您展示实际的生产级产品 例如，这些神经网络 看起来就是这样，为此我鼓励你 去这个网站看看，它很不错。 其中之一的可视化 网络，这就是你将要找到的。 在这个网站和这个神经网络中 这里指的是在生产环境中使用的情况。 它具有这种特殊的结构

### 0:23:24–0:23:54

EN：network is called the Transformer and this particular one as an example has 8 5,000 roughly parameters now here on the top we take the inputs which are the token sequences and then information flows through the neural network until the output which here are the logit softmax but these are the predictions for what comes next what token comes next and then here there's a sequence of Transformations and all these

中文：该网络被称为变压器（Transformer）， 例如，这个例子有8个。 大约5000 现在，我们在顶部取以下参数： 输入项即令牌 序列，然后是信息流 通过神经网络，直到 这里输出的是logit softmax函数。 但这些是对什么的预测 接下来是什么代币？ 接下来，这里有一系列…… 转变以及所有这些

### 0:23:54–0:24:20

EN：intermediate values that get produced inside this mathematical expression s it is sort of predicting what comes next so as an example these tokens are embedded into kind of like this distributed representation as it's called so every possible token has kind of like a vector that represents it inside the neural network so first we embed the tokens and then those values uh kind of like flow through this diagram and these are all

中文：产生的中间值 在这个数学表达式内部 这有点像是在预测接下来会发生什么，所以 例如，这些令牌是嵌入式的。 有点像这种分布式 所谓“代表”，就是如此。 可能的标记有点像一个向量 这代表了它在神经系统内部的状态。 所以首先我们将令牌嵌入到网络中， 那么这些值就有点像流量了。 通过这张图表，这些都是

### 0:24:20–0:24:44

EN：very simple mathematical Expressions individually so we have layer norms and Matrix multiplications and uh soft Maxes and so on so here kind of like the attention block of this Transformer and then information kind of flows through into the multi-layer perceptron block and so on and all these numbers here these are the intermediate values of the expression and uh you can almost think of these as kind of like the firing

中文：非常简单的数学表达式 因此，我们有层规范，并且 矩阵乘法和软极大值 等等，所以这里有点像…… 这个变压器的注意力阻塞和 然后信息就以这种方式流动起来。 进入多层感知器模块 等等，以及这里的所有数字。 这些是中间值 表情，呃，你几乎可以思考 这些就像是射击

### 0:24:44–0:25:06

EN：rates of these synthetic neurons but I would caution you to uh not um kind of think of it too much like neurons because these are extremely simple neurons compared to the neurons you would find in your brain your biological neurons are very complex dynamical processes that have memory and so on there's no memory in this expression it's a fixed mathematical expression from input to Output with no memory it's

中文：这些合成神经元的速率，但我 我会提醒你，呃，不要……嗯…… 别把它想得太像神经元了 因为这些都非常简单 与你的神经元相比，这些神经元 会在你的大脑中找到你的生物机能 神经元具有非常复杂的动力学特性。 具有内存等功能的进程 这个表达中没有记忆。 这是一个固定的数学表达式 从输入到输出，没有内存，它是

### 0:25:06–0:25:28

EN：just a stateless so these are very simple neurons in comparison to biological neurons but you can still kind of loosely think of this as like a synthetic piece of uh brain tissue if you if you like uh to think about it that way so information flows through all these neurons fire until we get to the predictions now I'm not actually going to dwell too much on the precise

中文：只是一个 无状态的，所以这些非常简单 与生物学相比，神经元 神经元，但你仍然可以某种程度上 可以粗略地将其理解为…… 如果是人造脑组织的话 如果你想的话，可以考虑一下。 这样信息就能流通了。 所有这些神经元都会放电，直到我们到达…… 现在的预测我其实并不相信 不会过于纠结于精确性。

### 0:25:28–0:25:52

EN：kind of like mathematical details of all these Transformations honestly I don't think it's that important to get into what's really important to understand is that this is a mathematical function it is uh parameterized by some fixed set of parameters like say 85,000 of them and it is a way of transforming inputs into outputs and as we twiddle the parameters we are getting uh different kinds of predictions and then we need to find a

中文：有点像所有数学细节 说实话，我并不理解这些转变。 我认为进入这个领域非常重要 真正需要理解的是…… 这是一个数学函数 呃，是由某些固定的参数集来定义的 例如，参数有 85,000 个， 它是将输入转化为输出的一种方式 输出结果以及我们调整参数的情况 我们正在接收各种不同的 做出预测，然后我们需要找到一个

### 0:25:52–0:26:14

EN：good setting of these parameters so that the predictions uh sort of match up with the patterns seen in training set so that's the Transformer okay so I've shown you the internals of the neural network and we talked a bit about the process of training it I want to cover one more major stage of working with these networks and that is the stage called inference so in inference what

中文：对这些参数进行良好设置，以便 预测结果与实际情况基本吻合 训练集中观察到的模式 这就是变形金刚，好的，我已经…… 向您展示了神经系统的内部结构 我们还聊了聊网络方面的事情。 我想介绍一下它的训练过程。 与……合作的又一个主要阶段 这些网络，这就是舞台。 称为推理，那么在推理中是什么

## 6. inference（0:26:01–0:31:09）

### 0:26:14–0:26:37

EN：we're doing is we're generating new data from the model and so uh we want to basically see what kind of patterns it has internalized in the parameters of its Network so to generate from the model is relatively straightforward we start with some tokens that are basically your prefix like what you want to start with so say we want to start with the token 91 well we feed it into

中文：我们正在做的就是生成新数据。 从模型来看，所以我们想要 基本上就是看看它呈现出什么样的模式。 已内化于以下参数中 它的网络由此产生 模型相对简单 我们首先从一些代币开始，这些代币是 基本上就是你想要的那个前缀。 首先，假设我们想开始 我们用代币 91 将其输入

### 0:26:37–0:27:03

EN：the network and remember that the network gives us probabilities right it gives us this probability Vector here so what we can do now is we can basically flip a biased coin so um we can sample uh basically a token based on this probability distribution so the tokens that are given High probability by the model are more likely to be sampled when you flip this biased coin you can think

中文：这 网络，并记住网络 它给我们提供了概率，对吧？ 这里是概率向量，所以我们…… 现在我们基本上可以翻转一个 有偏硬币，所以我们可以抽样。 基本上是基于此的令牌 概率分布，因此代币 被赋予高概率 当模型出现时，它们更有可能被抽样。 你抛掷这枚有偏见的硬币，你可以思考

### 0:27:03–0:27:25

EN：of it that way so we sample from the distribution to get a single unique token so for example token 860 comes next uh so 860 in this case when we're generating from model could come next now 860 is a relatively likely token it might not be the only possible token in this case there could be many other tokens that could have been sampled but we could see that 86c is a relatively

中文：就这样，我们从中抽样。 分发以获得唯一的 代币，例如代币 860 接下来，呃，所以在这种情况下是 860，当我们 接下来可能是基于模型的生成。 现在860是一个相对有可能的代币。 可能并非唯一可能的代币 这种情况可能还有其他类似情况。 可以进行采样但 我们可以看到，86c 是一个相对较高的温度。

### 0:27:25–0:27:49

EN：likely token as an example and indeed in our training examp example here 860 does follow 91 so let's now say that we um continue the process so after 91 there's a60 we append it and we again ask what is the third token let's sample and let's just say that it's 287 exactly as here let's do that again we come back in now we have a sequence of three and we

中文：可能的标记作为一个例子，而且确实如此 我们的培训示例在这里是 860。 按照91的指示，现在我们假设我们嗯 继续这个过程，这样在91之后就有了 a60 我们把它附加上去，然后我们再次询问什么 是第三个标记，让我们来采样一下。 我们就假设它是 287 吧。 来，我们再来一遍，我们回来。 现在我们有了三个数字的序列，我们

### 0:27:49–0:28:15

EN：ask what is the likely fourth token and we sample from that and get this one and now let's say we do it one more time we take those four we sample and we get this one and this 13659 uh this is not actually uh 3962 as we had before so this token is the token article uh instead so viewing a single article and so in this case we didn't

中文：询问第四个可能的标记是什么， 我们从中抽样，得到这个样本。 现在假设我们再做一次…… 选取我们抽样的这四个样本，我们得到 这个和这个 13659 呃，这实际上不是 3962 as 我们之前已经有了，所以这个令牌就是令牌。 文章呃，而不是查看单个 文章，所以在这个案例中我们没有。

### 0:28:15–0:28:40

EN：exactly reproduce the sequence that we saw here in the training data so keep in mind that these systems are stochastic they have um we're sampling and we're flipping coins and sometimes we lock out and we reproduce some like small chunk of the text and training set but sometimes we're uh we're getting a token that was not verbatim part of any of the documents in the training data so we're

中文：准确地重现我们……的序列 在训练数据中看到了这一点，所以请继续关注。 请注意，这些系统是随机的。 他们有，嗯，我们正在抽样，我们是 抛硬币，有时我们会锁定目标 我们复制了一些类似小块的内容。 文本和训练集，但 有时我们会收到一个令牌 那并非任何原文的一部分 训练数据中的文档，所以我们是

### 0:28:40–0:29:00

EN：going to get sort of like remixes of the data that we saw in the training because at every step of the way we can flip and get a slightly different token and then once that token makes it in if you sample the next one and so on you very quickly uh start to generate token streams that are very different from the token streams that UR in the training documents so

中文：将会得到一些类似混音的作品 我们在训练中看到的数据是因为 在每个环节我们都可以翻转和 获取一个略有不同的令牌，然后 一旦该令牌成功进入系统，如果你 试下一个，以此类推，你非常 快速开始生成令牌 与以下情况截然不同的溪流 UR 的令牌流 在培训文件中

### 0:29:00–0:29:24

EN：statistically they will have similar properties but um they are not identical to your training data they're kind of like inspired by the training data and so in this case we got a slightly different sequence and why would we get article you might imagine that article is a relatively likely token in the context of bar viewing single Etc and you can imagine that the word article followed this context window somewhere

中文：从统计学角度来看，它们将具有相似性。 它们都具有某些特性，但它们并不完全相同。 对于你的训练数据来说，它们有点像 就像受到训练数据的启发一样 所以，在这种情况下，我们得到了一个略微的 不同的顺序，为什么我们会得到 你可能会想象那篇文章 是一个相对可能的标记 酒吧浏览单页等的背景 你可以想象“文章”这个词。 随后，这个上下文窗口出现在某个地方。

### 0:29:24–0:29:49

EN：in the training documents uh to some extent and we just happen to sample it here at that stage so basically inference is just uh predicting from these distributions one at a time we continue feeding back tokens and getting the next one and we uh we're always flipping these coins and depending on how lucky or unlucky we get um we might get very different kinds of patterns depending on how we sample from these

中文：在培训文档中，呃，对一些人来说 范围很广，我们恰好对其进行了抽样调查。 就目前这个阶段而言，基本上 推理就是根据已知信息进行预测。 我们一次处理这些分布情况 继续反馈代币并获得 下一个，我们总是 抛掷这些硬币，并取决于 我们运气好还是不好，嗯，我们可能会 会得到非常不同的图案 这取决于我们如何从这些样本中抽样。

### 0:29:49–0:30:13

EN：probability distributions so that's inference so in most common scenarios uh basically downloading the internet and tokenizing it is is a pre-processing step you do that a single time and then uh once you have your token sequence we can start training networks and in Practical cases you would try to train many different networks of different kinds of uh settings and different kinds of arrangements and different kinds of

中文：概率分布就是这样。 所以，在大多数常见情况下，推理是…… 基本上就是从互联网下载 分词是预处理过程。 步骤一：你只需执行一次该步骤，然后 一旦你有了令牌序列，我们 可以开始训练网络，并且在 你会尝试训练的实际案例 许多不同的网络 各种设置和不同种类 各种安排和不同种类

### 0:30:13–0:30:33

EN：sizes and so you''ll be doing a lot of neural network training and um then once you have a neural network and you train it and you have some specific set of parameters that you're happy with um then you can take the model and you can do inference and you can actually uh generate data from the model and when you're on chat GPT and you're talking with a model uh that model is trained

中文：尺寸，所以你会做很多…… 神经网络训练，然后一旦 你有一个神经网络，然后你进行训练 它，而且你还有一些特定的集合 你满意的参数 然后你可以采用这个模型，然后你可以 进行推理，你实际上可以…… 从模型生成数据，并且当 你正在使用 GPT 聊天软件，并且正在聊天 用一个模型，呃，这个模型是训练过的

### 0:30:33–0:30:54

EN：and has been trained by open aai many months ago probably and they have a specific set of Weights that work well and when you're talking to the model all of that is just inference there's no more training those parameters are held fixed and you're just talking to the model sort of uh you're giving it some of the tokens and it's kind of completing token sequences and that's

中文：并接受过 Open AAI 的培训， 可能几个月前他们就…… 一组效果很好的特定重量 当你和模型对话时，所有 那只是推断，并没有确凿的证据。 更多训练将保留这些参数。 问题已解决，你只是在和……说话。 模型有点像，呃，你给它一些 这些代币，而且有点像 完成令牌序列，就完成了。

### 0:30:54–0:31:14

EN：what you're seeing uh generated when you actually use the model on CH GPT so that model then just does inference alone so let's now look at an example of training an inference that is kind of concrete and gives you a sense of what this actually looks like uh when these models are trained now the example that I would like to work with and that I'm particularly fond of is that of opening

中文：你现在看到的，呃，是在你……时生成的 实际上，我们在 CH GPT 上使用了该模型。 然后模型就只进行推理了。 现在我们来看一个训练的例子。 一个相当具体的推论 并让你感受到这是什么。 实际上看起来像……呃，当这些模型 现在接受的训练就是我的例子。 我喜欢和他们一起工作，而且我是 特别喜欢的是开场白

## 7. GPT-2: training and inference（0:31:09–0:42:52）

### 0:31:14–0:31:39

EN：eyes gpt2 so GPT uh stands for generatively pre-trained Transformer and this is the second iteration of the GPT series by open AI when you are talking to chat GPT today the model that is underlying all of the magic of that interaction is GPT 4 so the fourth iteration of that series now gpt2 was published in 2019 by openi in this paper that I have right here and the reason I

中文：眼睛 gpt2 所以 GPT 呃代表 生成式预训练的Transformer和 这是 GPT 的第二个版本。 OpenAI 的系列节目，当你在说话时 今天来聊聊GPT，这个模型是 这一切魔力的根源就在于此。 交互是 GPT 4，所以是第四个 该系列的迭代版本现在是gpt2。 本文由 openi 于 2019 年发表。 我手里就有这个，而我的理由是……

### 0:31:39–0:32:00

EN：like gpt2 is that it is the first time that a recognizably modern stack came together so um all of the pieces of gpd2 are recognizable today by modern standards it's just everything has gotten bigger now I'm not going to be able to go into the full details of this paper of course because it is a technical publication but some of the details that I would like to highlight

中文：就像 GPT-2 一样，这是第一次 一个明显具有现代感的堆栈出现了 把所有GPD2的组成部分加在一起。 如今，现代人都能识别出它们。 标准就是一切都有标准。 现在我变大了，我不会再这样了。 能够详细阐述这一点。 当然是纸质的，因为它是一张…… 技术出版物，但其中一些 我想重点强调的细节

### 0:32:00–0:32:28

EN：are as follows gpt2 was a Transformer neural network just like you were just like the neural networks you would work with today it was it had 1.6 billion parameters right so these are the parameters that we looked at here it would have 1.6 billion of them today modern Transformers would have a lot closer to a trillion or several hundred billion probably the maximum context length here was 1,24 tokens so it is when we are

中文：具体来说，gpt2 是一个 Transformer。 就像你一样，神经网络也刚刚 就像你将要工作的神经网络一样 截至今天，它拥有16亿 参数没错，这些就是…… 我们在这里考察的参数是 如今将有16亿人。 现代变形金刚会有很多 接近万亿或几百万亿 十亿 这可能是此处上下文的最大长度。 是 1.24 个代币，所以当我们是

### 0:32:28–0:32:53

EN：sampling chunks of Windows of tokens from the data set we're never taking more than 1,24 tokens and so when you are trying to predict the next token in a sequence you will never have more than 1,24 tokens uh kind of in your context in order to make that prediction now this is also tiny by modern standards today the token uh the context lengths would be a lot closer to um couple

中文：对令牌窗口块进行采样 从我们从未取用过的数据集中 超过 1.24 个代币，所以当你 试图预测下一个标记 你永远不会拥有超过一个序列 1.24 个标记，嗯，有点像你的意思 为了现在做出预测 按现代标准来看，这也非常小。 今天，令牌的上下文长度 会更接近于一对夫妇。

### 0:32:53–0:33:12

EN：hundred thousand or maybe even a million and so you have a lot more context a lot more tokens in history history and you can make a lot better prediction about the next token in the sequence in that way and finally gpt2 was trained on approximately 100 billion tokens and this is also fairly small by modern standards as I mentioned the fine web data set that we looked at here the fine

中文：十万，甚至可能一百万。 因此，你就能获得更多背景信息。 历史上的更多代币，还有你 可以做出更准确的预测 序列中的下一个标记 最后，GPT2 以这种方式进行训练。 大约1000亿个代币和 按现代标准来看，这也相当小。 正如我之前提到的，网络标准非常高。 我们在这里查看的数据集是精细的。

### 0:33:12–0:33:41

EN：web data set has 15 trillion tokens uh so 100 billion is is quite small now uh I actually tried to reproduce uh gpt2 for fun as part of this project called lm. C so you can see my rup of doing that in this post on GitHub under the lm. C repository so in particular the cost of training gpd2 in 2019 what was estimated to be approximately $40,000 but today you can do

中文：网络数据集包含 15 万亿个代币。 所以1000亿相当可观。 小的 现在，呃，我试着重现了一下。 作为本项目的一部分，我使用 gpt2 进行娱乐。 名为lm。 C，所以你可以看到我的 rup 在 GitHub 上的这篇文章中，我们这样做了。 电影。 C 存储库，特别是 2019年GPD2训练的成本是多少？ 估计约为 4万美元，但今天你可以做到

### 0:33:41–0:34:05

EN：significantly better than that and in particular here it took about one day and about $600 uh but this wasn't even trying too hard I think you could really bring this down to about $100 today now why is it that the costs have come down so much well number one these data sets have gotten a lot better and the way we filter them extract them and prepare them has gotten a lot more refined and

中文：比那好得多，而且 特别是在这里，大约花了一天时间。 以及关于 600美元，呃，但这根本就没尽力。 我觉得你真的可以做到这一点 今天跌到大约100美元了，这是为什么呢？ 成本已经大幅下降了。 首先，这些数据集有 情况好转了很多，我们的方式也改变了。 过滤、提取并制备 它们变得更加精细化了，

### 0:34:05–0:34:27

EN：so the data set is of just a lot higher quality so that's one thing but really the biggest difference is that our computers have gotten much faster in terms of the hardware and we're going to look at that in a second and also the software for uh running these models and really squeezing out all all the speed from the hardware as it is possible uh that software has also gotten much

中文：所以这个数据集要高得多。 质量是一方面，但实际上 最大的区别在于我们的 计算机的运行速度已经大大加快了。 硬件方面，我们将…… 稍等片刻，还有…… 用于运行这些模型的软件 真正榨干所有速度 从硬件方面来看，这是可能的。 该软件也得到了极大的发展。

### 0:34:27–0:34:46

EN：better as as everyone has focused on these models and try to run them very very quickly now I'm not going to be able to go into the full detail of this gpd2 reproduction and this is a long technical post but I would like to still give you an intuitive sense for what it looks like to actually train one of these models as a researcher like what are you looking at and what does it look

中文：情况越来越好，因为大家都专注于 这些模型，并尝试运行它们。 非常 现在我没办法很快…… 详细了解一下GPD2 繁殖，这是一个漫长的过程。 这是一篇技术性文章，但我仍然想…… 让你对它有直观的了解 看起来确实需要训练其中一个 这些模型作为研究者来说，比如什么 你在看什么？它看起来怎么样？

### 0:34:46–0:35:11

EN：like what does it feel like so let me give you a sense of that a little bit okay so this is what it looks like let me slide this over so what I'm doing here is I'm training a gpt2 model right now and um what's happening here is that every single line here like this one is one update to the model so remember how here we are um basically making the

中文：那感觉究竟如何？让我来告诉你。 让你稍微体会一下那种感觉 好的，这就是它的样子。 我滑进去这个 结束了，所以我现在在这里做的是…… 正在训练 GPT2 模型 嗯，这里发生的事情是这样的： 这里的每一行，像这样的，都是 模型更新，请记住如何 我们现在基本上是在做……

### 0:35:12–0:35:35

EN：prediction better for every one of these tokens and we are updating these weights or parameters of the neural net so here every single line is One update to the neural network where we change its parameters by a little bit so that it is better at predicting next token and sequence in particular every single line here is improving the prediction on 1 million tokens in the training set so

中文：对于所有这些预测，预测效果都会更好。 我们正在更新这些权重。 或者说神经网络的参数，所以这里 每一行都是一次更新 我们改变神经网络的 稍微调整一下参数，使其成为 更擅长预测下一个词元和 序列，尤其是每一行 这里是对预测结果的改进（1）。 训练集中有数百万个标记，因此

### 0:35:35–0:36:00

EN：we've basically taken 1 million tokens out of this data set and we've tried to improve the prediction of that token as coming next in a sequence on all 1 million of them simultaneously and at every single one of these steps we are making an update to the network for that now the number to watch closely is this number called loss and the loss is a single number

中文：我们基本上已经获得了100万个代币。 从这个数据集中，我们已经尝试过…… 提高对该标记的预测能力 接下来是所有 1 的序列。 其中数百万 同时，在每一个 我们正在对这些步骤进行更新 现在该号码已加入网络 需要密切关注的这个数字叫做 损失，且损失是一个单独的数字

### 0:36:00–0:36:22

EN：that is telling you how well your neural network is performing right now and it is created so that low loss is good so you'll see that the loss is decreasing as we make more updates to the neural nut which corresponds to making better predictions on the next token in a sequence and so the loss is the number that you are watching as a neural network researcher and you are kind of

中文：这说明你的神经系统状况如何 网络目前运行正常。 这样做的目的是为了降低损失，所以低损失是好事。 你会发现损失正在减少。 随着我们对神经网络进行更多更新 坚果对应于制造更好的 对下一个代币的预测 序列，因此损失是数字 你正在观察的是一个神经系统 网络研究员，你有点像

### 0:36:22–0:36:50

EN：waiting you're twiddling your thumbs uh you're drinking coffee and you're making sure that this looks good so that with every update your loss is improving and the network is getting better at prediction now here you see that we are processing 1 million tokens per update each update takes about 7 Seconds roughly and here we are going to process a total of 32,000 steps of optimization so 32,000 steps with 1

中文：你等着呢，闲着没事干嘛？ 你一边喝咖啡一边制作 确保这看起来不错，这样…… 每次更新后，你的损失都在减少。 网络正在变得越来越好 现在预测一下，你可以看到我们是 每次更新处理 100 万个代币 每次更新大约需要7秒钟。 大致如此，接下来我们将进行处理。 总共走了32000步 优化过程共 32,000 步，步数为 1

### 0:36:50–0:37:15

EN：million tokens each is about 33 billion tokens that we are going to process and we're currently only about 420 step 20 out of 32,000 so we are still only a bit more than 1% done because I've only been running this for 10 or 15 minutes or something like that now every 20 steps I have configured this optimization to do inference so what you're seeing here is the model is predicting the next token

中文：每百万个代币大约是330亿 我们将要处理的令牌和 我们目前只完成了大约 420 步 20 总共32000人，所以我们仍然只差一点点。 完成度超过1%，因为我只…… 运行此程序 10 或 15 分钟，或 类似 现在我每走20步就有 配置此优化以执行以下操作 推断，所以你在这里看到的是 该模型正在预测下一个词元

### 0:37:15–0:37:37

EN：in a sequence and so you sort of start it randomly and then you continue plugging in the tokens so we're running this inference step and this is the model sort of predicting the next token in the sequence and every time you see something appear that's a new token um so let's just look at this and you can see that this is not yet very coherent and keep in mind that this is

中文：按顺序，然后你就开始了。 它随机出现，然后你继续 插入令牌，所以我们正在运行 这一推理步骤，这就是 该模型类似于预测下一个词元。 在序列中，每次你看到 出现了一些新的东西 令牌，嗯，所以我们来看看这个， 你可以看出这还不太成熟。 连贯一致，并且记住这是

### 0:37:37–0:37:59

EN：only 1% of the way through training and so the model is not yet very good at predicting the next token in the sequence so what comes out is actually kind of a little bit of gibberish right but it still has a little bit of like local coherence so since she is mine it's a part of the information should discuss my father great companions Gordon showed me sitting over at and Etc

中文：训练才进行了1%， 所以这个模型目前还不太好。 预测下一个标记 顺序，所以最终出来的结果是 有点像胡言乱语，对吧？ 但它仍然带有一点类似的东西 局部一致性，所以既然她是我的。 这是信息的一部分。 谈谈我父亲的伟大伙伴们 戈登带我看了看坐在那里等等

### 0:37:59–0:38:23

EN：so I know it doesn't look very good but let's actually scroll up and see what it looked like when I started the optimization so all the way here at step one so after 20 steps of optimization you see that what we're getting here is looks completely random and of course that's because the model has only had 20 updates to its parameters and so it's giving you random text because it's a

中文：我知道它看起来不太好，但是 我们向上滚动看看吧。 看起来就像我开始的时候 优化一直持续到这里 步 经过 20 步优化后， 你看，我们在这里得到的是…… 看起来完全随机，当然 那是因为该型号只有20个型号。 对其参数进行更新，因此是 给你随机文本，因为它是一个

### 0:38:23–0:38:49

EN：random Network and so you can see that at least in comparison to this model is starting to do much better and indeed if we waited the entire 32,000 steps the model will have improved the point that it's actually uh generating fairly coherent English uh and the tokens stream correctly um and uh they they kind of make up English a a lot better um so this has to run for about a day or

中文：随机网络，所以你可以看到 至少与这个模型相比是 情况开始好转，而且确实如此 我们等了整整32000步。 该模型将改进这一点，即 实际上，它正在产生相当可观的产量。 连贯的英语呃和标记 正确地播放，嗯，还有，他们 很多英语都是自己编造的。 更好的 嗯，所以这需要运行大约一天，或者

### 0:38:49–0:39:12

EN：two more now and so uh at this stage we just make sure that the loss is decreasing everything is looking good um and we just have to wait and now um let me turn now to the um story of the computation that's required because of course I'm not running this optimization on my laptop that would be way too expensive uh because we have to run this neural network and we have to

中文：现在还有两个，所以，嗯，在这个阶段我们 只需确保损失是 所有指标都在下降，看起来不错。 我们只需要等待 现在，嗯，让我转向…… 所需计算的故事 因为我当然不会运营这个。 对我的笔记本电脑进行优化，应该是 太贵了，呃，因为我们必须 运行这个神经网络，我们需要……

### 0:39:12–0:39:30

EN：improve it and we have we need all this data and so on so you can't run this too well on your computer uh because the network is just too large uh so all of this is running on the computer that is out there in the cloud and I want to basically address the compute side of the store of training these models and what that looks like so let's take a

中文：改进它，我们需要这一切。 数据等等，所以你也不能运行这个程序。 嗯，在你的电脑上，因为 网络规模太大了，所以所有的一切 这是在一台电脑上运行的。 我在云端，我想 主要解决计算方面的问题 训练这些模型的存储和 那看起来是什么样的呢？我们来看一个例子。

### 0:39:30–0:39:52

EN：look okay so the computer that I'm running this optimization on is this 8X h100 node so there are eight h100s in a single node or a single computer now I am renting this computer and it is somewhere in the cloud I'm not sure where it is physically actually the place I like to rent from is called Lambda but there are many other companies who provide this service so

中文：看起来没问题，所以我的电脑是 运行此优化是在 8 倍速上进行的。 h100 节点，所以一个节点中有八个 h100。 现在我只有一个节点或一台计算机。 我租用了这台电脑，它是 我不确定是在云端的某个地方。 它实际所在的物理位置是 我喜欢租房的地方叫做 Lambda，但还有许多其他的 提供这项服务的公司

### 0:39:52–0:40:18

EN：when you scroll down you can see that uh they have some on demand pricing for um sort of computers that have these uh h100s which are gpus and I'm going to show you what they look like in a second but on demand 8times Nvidia h100 uh GPU this machine comes for $3 per GPU per hour for example so you can rent these and then you get a machine in a

中文：向下滚动后，你可以看到…… 他们有一些按需定价的产品 嗯，就是那种有这些功能的电脑。 h100s是GPU，我打算 几秒钟就能让你看到它们的样子。 但按需使用 8 倍 Nvidia h100 呃 这台机器的GPU售价为每块3美元。 例如按小时计费，这样你就可以租用 这些，然后你就能得到一台机器了。

### 0:40:18–0:40:42

EN：cloud and you can uh go in and you can train these models and these uh gpus they look like this so this is one h100 GPU uh this is kind of what it looks like and you slot this into your computer and gpus are this uh perfect fit for training your networks because they are very computationally expensive but they display a lot of parallelism in the computation so you can have many

中文：云端，你可以进去，你可以 训练这些 这些模型和这些GPU看起来像 所以这是一块H100 GPU，嗯，这是 看起来大概就是这样，然后你就可以插孔了。 这需要插入你的电脑和显卡中。 这非常适合训练你的 网络，因为它们非常 计算成本高昂，但它们 在很多方面都展现出平行性 计算，所以你可以有很多

### 0:40:42–0:41:07

EN：independent workers kind of um working all at the same time in solving uh the matrix multiplication that's under the hood of training these neural networks so this is just one of these h100s but actually you would put them you would put multiple of them together so you could stack eight of them into a single node and then you can stack multiple nodes into an entire data center or an entire system

中文：独立工作者，嗯，工作 同时解决呃 矩阵乘法，即以下部分 训练这些神经元的罩子 网络，所以这只是其中之一。 h100s，但实际上你会把它们放进去。 你会把它们中的多个放在一起。 所以你可以把它们中的八个堆叠起来。 单节点，然后您可以堆叠 将多个节点整合到一个完整的数据中 中心或整个系统

### 0:41:07–0:41:28

EN：so when we look at a data center can't spell when we look at a data center we start to see things that look like this right so we have one GPU goes to eight gpus goes to a single system goes to many systems and so these are the bigger data centers and there of course would be much much more expensive um and what's happening is that all the

中文：所以当我们查看数据时 当我们看着一个中心时，它无法拼写出来。 在数据中心，我们开始看到一些事情…… 看起来是这样，所以我们有一个GPU。 到八个GPU到单个 系统连接到许多系统，因此这些 是规模更大的数据中心，而且 当然，费用会高得多。 嗯，现在的情况是，所有这些

### 0:41:28–0:41:55

EN：big tech companies really desire these gpus so they can train all these language models because they are so powerful and that has is fundamentally what has driven the stock price of Nvidia to be $3.4 trillion today as an example and why Nvidia has kind of exploded so this is the Gold Rush the Gold Rush is getting the gpus getting enough of them so they can all collaborate to perform this optimization

中文：大型科技公司真的很想要这些 GPU，这样它们就可以训练所有这些模型。 语言模型，因为它们如此 强大且具有根本性的 是什么因素推动了股价上涨？ 英伟达今天的市值将达到3.4万亿美元。 举例说明以及为什么英伟达有某种…… 爆发式增长，这就是淘金热。 淘金热正在让GPU变得…… 足够多的，这样他们就能全部 协作完成此优化

### 0:41:55–0:42:16

EN：and they're what are they all doing they're all collaborating to predict the next token on a data set like the fine web data set this is the computational workflow that that basically is extremely expensive the more gpus you have the more tokens you can try to predict and improve on and you're going to process this data set faster and you can iterate faster and get a bigger Network and

中文：他们都在做什么？ 他们都在合作预测 下一个标记在类似罚款的数据集上 网络数据 这是计算工作流程 那基本上是非常 GPU越多，成本越高。 您可以尝试预测更多代币，并且 改进并进行处理 这个数据集速度更快，而且你可以迭代。 速度更快，网络覆盖范围更广

### 0:42:16–0:42:38

EN：train a bigger Network and so on so this is what all those machines are look like are uh are doing and this is why all of this is such a big deal and for example this is a article from like about a month ago or so this is why it's a big deal that for example Elon Musk is getting 100,000 gpus uh in a single Data Center and all

中文：训练一个更大的网络，以此类推，如此循环往复。 这就是所有这些机器的样子 我们正在做，这就是为什么所有的一切 这可是件大事，例如 这是 大约一个月前的文章 所以这就是为什么这件事意义重大的原因。 例如，埃隆·马斯克获得了100,000美元。 GPU 在单个数据中心内，所有

### 0:42:38–0:42:57

EN：of these gpus are extremely expensive are going to take a ton of power and all of them are just trying to predict the next token in the sequence and improve the network uh by doing so and uh get probably a lot more coherent text than what we're seeing here a lot faster okay so unfortunately I do not have a couple 10 or hundred million of dollars to

中文：这些GPU价格极其昂贵。 将会消耗大量的电力等等 他们只是想预测…… 序列中的下一个标记并改进 通过这样做，网络就能获得 可能比这更连贯的文本 我们看到的情况是速度快得多，好的。 所以很遗憾，我没有几对。 1000万或1亿美元

## 8. Llama 3.1 base model inference（0:42:52–0:59:23）

### 0:42:57–0:43:17

EN：spend on training a really big model like this but luckily we can turn to some big tech companies who train these models routinely and release some of them once they are done training so they've spent a huge amount of compute to train this network and they release the network at the end of the optimization so it's very useful because they've done a lot of compute for that

中文：花费大量资金训练一个非常大的模型 就像这样，但幸运的是我们可以转向 一些大型科技公司会培训这些人 模型定期发布一些 他们训练结束后就会这样 他们花费了大量的计算资源 训练这个网络，然后他们发布 末端的网络 优化因此非常有用，因为 他们为此做了大量的计算工作。

### 0:43:18–0:43:39

EN：so there are many companies who train these models routinely but actually not many of them release uh these what's called base models so the model that comes out at the end here is is what's called a base model what is a base model it's a token simulator right it's an internet text token simulator and so that is not by itself useful yet because what we want is what's called an

中文：所以有很多公司提供培训。 这些模型通常，但实际上并非如此。 他们中的许多人发布了这些，呃，这是什么？ 称为基础模型，因此该模型 最后出来的就是这个。 基础模型是什么？ 这是一个代币模拟器，对吧？ 互联网文本令牌模拟器等等 这本身还没有什么用处，因为 我们想要的是一个叫做……的东西

### 0:43:39–0:44:01

EN：assistant we want to ask questions and have it respond to answers these models won't do that they just uh create sort of remixes of the internet they dream internet pages so the base models are not very often released because they're kind of just only a step one of a few other steps that we still need to take to get in system however a few releases have been made so

中文：助理，我们想问一些问题， 让它对这些模型的答案做出回应 他们不会那样做，他们只是……创建排序 他们梦想着互联网的混音 网页，所以基础模型是 由于它们不常发行，所以发行频率不高。 这只是几个步骤中的第一步。 我们还需要采取其他步骤。 进入系统 然而，也有一些版本已经发布。

### 0:44:01–0:44:30

EN：as an example the gbt2 model released the 1.6 billion sorry 1.5 billion model back in 2019 and this gpt2 model is a base model now what is a model release what does it look like to release these models so this is the gpt2 repository on GitHub well you need two things basically to release model number one we need the um python code usually that describes the sequence of operations in

中文：例如，发布的GBT2模型。 16亿，抱歉，是15亿模型 早在2019年，这个gpt2模型就是 基本模型现在是什么？模型发布 发布这些内容会是什么样子？ 模型，所以这是 gpt2 存储库。 GitHub，你需要两样东西。 基本上，我们发布第一款模型 通常需要的是Python代码。 描述了操作顺序

### 0:44:30–0:44:55

EN：detail that they make in their model so um if you remember back this Transformer the sequence of steps that are taken here in this neural network is what is being described by this code so this code is sort of implementing the what's called forward pass of this neural network so we need the specific details of exactly how they wired up that neural network so this is just

中文：他们在模型中制作的细节 嗯，如果你还记得的话 回到这个 转换步骤顺序 这里所采用的神经网络是 这段代码描述的是什么？ 这段代码某种程度上实现了…… 这叫做前向传递 所以我们需要特定的神经网络。 它们具体是如何连接的细节 那个神经网络，所以这只是

### 0:44:55–0:45:17

EN：computer code and it's usually just a couple hundred lines of code it's not it's not that crazy and uh this is all fairly understandable and usually fairly standard what's not standard are the parameters that's where the actual value is what are the parameters of this neural network because there's 1.6 billion of them and we need the correct setting or a really good setting and so that's why in addition to this source

中文：计算机代码，通常只是一个 几百行代码而已，不是这样的。 其实也没那么疯狂，嗯，就这些了。 相当容易理解，而且通常也相当 标准是什么？非标准是什么？ 参数，也就是实际值所在的地方 这个参数是什么？ 神经网络，因为有 1.6 其中有数十亿，我们需要正确的 环境，或者说非常好的环境，等等 所以除了这个来源之外，还有

### 0:45:17–0:45:44

EN：code they release the parameters which in this case is roughly 1.5 billion parameters and these are just numbers so it's one single list of 1.5 billion numbers the precise and good setting of all the knobs such that the tokens come out well so uh you need those two things to get a base model release now gpt2 was released but that's actually a fairly old model as I

中文：它们通过代码释放参数，这些参数 在这种情况下，大约是15亿。 参数，这些只是数字而已。 这是一份包含15亿人的单一名单。 数字的精确和良好设置 所有旋钮都对准了代币。 出去 所以，你需要这两样东西。 获取基础型号 发布 现在GPT-2已经发布了，但那只是…… 实际上，这是一个相当老的型号，因为我

### 0:45:44–0:46:07

EN：mentioned so actually the model we're going to turn to is called llama 3 and that's the one that I would like to show you next so llama 3 so gpt2 again was 1.6 billion parameters trained on 100 billion tokens Lama 3 is a much bigger model and much more modern model it is released and trained by meta and it is a 45 billion parameter model trained on 15

中文：前面提到过，所以实际上我们采用的模型是 即将变成的叫做羊驼3， 这就是我想展示的那一个。 你下一个，所以羊驼3，所以gpt2又来了 在 100 个数据集上训练了 16 亿个参数 十亿代币 Lama 3 规模更大 这款模型，而且是更现代的型号。 由 meta 发布和训练，它是一款 基于 15 个数据集训练的 450 亿参数模型

### 0:46:07–0:46:33

EN：trillion tokens in very much the same way just much much bigger um and meta has also made a release of llama 3 and that was part of this paper so with this paper that goes into a lot of detail the biggest base model that they released is the Lama 3.1 4.5 405 billion parameter model so this is the base model and then in addition to the base model you see here

中文：万亿代币，情况非常相似 太多了 更大的嗯，而且元也做出了一个 发布《羊驼3》是其中的一部分 这 所以，这张纸就属于这个范畴。 很多细节，最大的基础模型 他们发布的是 Lama 3.1 4.5。 4050亿参数模型，所以这是 基础模型，然后在此基础上…… 您在这里看到的基本型号

### 0:46:33–0:46:53

EN：foreshadowing for later sections of the video they also released the instruct model and the instruct means that this is an assistant you can ask it questions and it will give you answers we still have yet to cover that part later for now let's just look at this base model this token simulator and let's play with it and try to think about you know what is this thing and how does it work and

中文：为后面的章节埋下伏笔 他们还发布了一段视频作为指导。 模型和指令意味着这 它是一个助手，你可以向它提问。 它会给你我们仍然想知道的答案。 稍后会介绍这部分内容。 现在我们来看一下这个基础模型。 这个代币模拟器，我们来玩玩吧 试着想想，你知道吗？ 这是什么？它是如何运作的？

### 0:46:53–0:47:14

EN：um what do we get at the end of this optimization if you let this run Until the End uh for a very big neural network on a lot of data so my favorite place to interact with the base models is this um company called hyperbolic which is basically serving the base model of the 405b Llama 3.1 so when you go to the website and I think you may have to

中文：嗯，我们最终会得到什么呢？ 如果让它运行直到优化完成 结束语，呃，对于一个非常大的神经网络 因为有很多数据，所以我最喜欢去的地方是 与基础模型交互是这个吗？ 公司名为hyperbolic， 基本上服务于基础模型 405b Llama 3.1 所以当你去到 网站，我觉得你可能需要……

### 0:47:14–0:47:34

EN：register and so on make sure that in the models make sure that you are using llama 3.1 405 billion base it must be the base model and then here let's say the max tokens is how many tokens we're going to be gener rating so let's just decrease this to be a bit less just so we don't waste compute we just want the next 128 tokens and leave the other

中文：注册等等，确保在……中 模特们请确保您正在使用 羊驼 3.1 4050 亿基础它必须是 基础模型，然后这里我们假设 最大代币数是我们拥有的代币数量。 将会是普通级影片，所以我们就…… 稍微减少一点这个量 我们不浪费计算资源，我们只想要 接下来128个代币，然后留下其他代币。

### 0:47:34–0:47:56

EN：stuff alone I'm not going to go into the full detail here um now fundamentally what's going to happen here is identical to what happens here during inference for us so this is just going to continue the token sequence of whatever you prefix you're going to give it so I want to first show you that this model here is not yet an assistant so you can for example ask it what is 2 plus 2 it's not

中文：光是这些事情我就不细说了。 详情如下：嗯，现在从根本上来说 接下来发生的事情与此完全相同。 这里在推理过程中发生了什么 对我们来说，这种情况还会继续下去。 任何你 你要给它加个前缀，所以我想要 首先向您展示这个模型 还不是助理，所以你可以…… 例如，问它2加2等于多少，它回答不是。

### 0:47:56–0:48:14

EN：going to tell you oh it's four uh what else can I help you with it's not going to do that because what is 2 plus 2 is going to be tokenized and then those tokens just act as a prefix and then what the model is going to do now is just going to get the probability for the next token and it's just a glorified autocomplete it's a very very expensive

中文：我要告诉你哦，是四，呃，什么 还有什么我可以帮到你的吗？它好像出问题了。 这样做是因为 2 加 2 等于多少？ 将被代币化，然后是这些 标记仅用作前缀，然后 该模型接下来要做的事情是： 我只是来获取概率 下一个代币，它只不过是一个高级版的代币而已。 自动补全功能非常非常昂贵。

### 0:48:14–0:48:39

EN：autocomplete of what comes next um depending on the statistics of what it saw in its training documents which are basically web pages so let's just uh hit enter to see what tokens it comes up with as a continuation okay so here it kind of actually answered the question and started to go off into some philosophical territory uh let's try it again so let me copy and paste and let's

中文：自动补全接下来要说什么？嗯 根据统计数据来看，它 在它的培训文件中看到了这些内容 基本上是网站 页面，所以我们直接按回车键看看吧。 它会生成哪些令牌？ 好的，接下来是…… 实际上回答了这个问题 开始偏离主题 哲学领域，嗯，我们来试试。 让我再复制粘贴一下，我们开始吧。

### 0:48:39–0:48:45

EN：try again from scratch what is 2 plus

中文：从头再试一次，2加起来等于多少？

### 0:48:49–0:49:08

EN：two so okay so it just goes off again so notice one more thing that I want to stress is that the system uh I think every time you put it in it just kind of starts from scratch so it doesn't uh the system here is stochastic so for the same prefix of tokens we're always getting a different answer and the reason for that is that we get this probity distribution and we

中文：两个，好吧，它又响了。 还有一点我想提醒大家： 压力就是这个系统，呃，我想 每次你把它放进去，它就有点…… 从零开始 所以，呃，这里的系统是 随机的，所以对于相同的前缀 我们总是会收到不同的代币。 答案是，原因如下： 我们得到了这个诚信分布，然后我们

### 0:49:08–0:49:35

EN：sample from it and we always get different samples and we sort of always go into a different territory uh afterwards so here in this case um I don't know what this is let's try one more time so it just continues on so it's just doing the stuff that it's saw on the internet right um and it's just kind of like regurgitating those uh statistical patterns so first things it's not an

中文：从中抽取样本，我们总能得到 不同的样本，我们总是 进入另一个领域 之后，所以在这个例子中，嗯，我 不知道这是什么，我们来试一个。 更多的 时间就这样继续下去，就是这样。 只是做它已经看到的事情而已。 互联网，嗯，就是这样。 就像反刍那些呃 统计 模式，所以首先它不是……

### 0:49:35–0:50:01

EN：assistant yet it's a token autocomplete and second it is a stochastic system now the crucial thing is that even though this model is not yet by itself very useful for a lot of applications just yet um it is still very useful because in the task of predicting the next token in the sequence the model has learned a lot about the world and it has stored all that knowledge in the parameters of

中文：助手，但它是一个令牌自动完成 其次，它现在是一个随机系统。 关键在于，尽管 这个模型本身还不太成熟。 对很多应用场景都很有用 然而，它仍然非常有用，因为 在预测下一个词元的任务中 在序列中，模型已经学习到 它储存了很多关于世界的信息，并且已经保存了很多。 所有这些知识都包含在以下参数中：

### 0:50:01–0:50:27

EN：the network so remember that our text looked like this right internet web pages and now all of this is sort of compressed in the weights of the network so you can think of um these 405 billion parameters is a kind of compression of the internet you can think of the 45 billion parameters is kind of like a zip file uh but it's not a loss less compression it's a loss C compression

中文：网络，所以请记住我们的文本 看起来就像这样，互联网网站 页面，现在这一切都有点像…… 压缩在网络权重中 所以你可以想想这4050亿。 参数是一种压缩方式 你能想到的互联网 450亿个参数有点像…… 压缩文件，但是它并非无损压缩。 压缩是一种损失 C 压缩

### 0:50:27–0:50:52

EN：we're kind of like left with kind of a gal of the internet and we can generate from it right now we can elicit some of this knowledge by prompting the base model uh accordingly so for example here's a prompt that might work to elicit some of that knowledge that's hiding in the parameters here's my top 10 list of the top landmarks to see in the pairs um and I'm doing it this way because I'm

中文：我们现在有点像是剩下了一种…… 互联网女孩，我们可以生成 我们现在可以从中引申出一些信息 通过提示基础来获得这种知识 相应地建模，例如 这里有一个可能有效的提示 引出其中的一些知识 隐藏在参数中的是我的首选 十大必游地标 这 对 嗯，我这样做是因为……

### 0:50:52–0:51:12

EN：trying to Prime the model to now continue this list so let's see if that works when I press enter okay so you see that it started a list and it's now kind of giving me some of those landmarks and now notice that it's trying to give a lot of information here now you might not be able to actually fully trust some of the information here remember that this is all just a

中文：尝试将模型准备到现在 继续列这个清单，看看是否如此。 按下按钮后即可工作 输入好的，你看它已经开始了。 清单，现在它有点给我一些启发 那些 地标建筑，现在请注意它是 这里试图提供很多信息。 现在你可能无法真正做到 这里的一些信息我完全信任。 记住，这一切都只是……

### 0:51:12–0:51:34

EN：recollection of some of the internet documents and so the things that occur very frequently in the internet data are probably more likely to be remembered correctly compared to things that happen very infrequently so you can't fully trust some of the things that and some of the information that is here because it's all just a vague recollection of Internet documents because the information is not stored explicitly in

中文：回忆起一些互联网 文件以及由此产生的事情 互联网数据中经常出现的情况是 可能更容易被记住 与发生的事情进行恰当的比较 非常少见，所以你无法完全 相信某些事，以及一些事 这里的信息是因为 这一切都只是模糊的记忆。 因为互联网文档 信息并未显式存储在

### 0:51:34–0:51:57

EN：any of the parameters it's all just the recollection that said we did get something that is probably approximately correct and I don't actually have the expertise to verify that this is roughly correct but you see that we've elicited a lot of the knowledge of the model and this knowledge is not precise and exact this knowledge is vague and probabilistic and statistical and the kinds of things that occur often are the

中文：任何参数都只是…… 回忆说，我们确实得到了 某种东西大概是 没错，但我实际上并没有 具备专业知识以验证这大致是 没错，但你看我们已经引发了 该模型的许多知识以及 这种知识并不精确。 这种知识很模糊，而且 概率论和统计学以及 经常发生的事情类型有：

### 0:51:57–0:52:19

EN：kinds of things that are more likely to be remembered um in the model now I want to show you a few more examples of this model's Behavior the first thing I want to show you is this example I went to the Wikipedia page for zebra and let me just copy paste the first uh even one sentence here and let me put it here now when I click enter what kind of uh completion

中文：更有可能发生的事情 记住，嗯，现在我想在模型中记住这一点 为了向您展示更多此类例子， 模型的行为是我首先想要的 我举这个例子来给你说明，我去了…… 斑马的维基百科页面，让我 直接复制粘贴第一个，呃，甚至一个 句子 就在这里，我现在把它放在这里。 点击输入什么类型的完成

### 0:52:19–0:52:46

EN：are we going to get so let me just hit enter there are three living species etc etc what the model is producing here is an exact regurgitation of this Wikipedia entry it is reciting this Wikipedia entry purely from memory and this memory is stored in its parameters and so it is possible that at some point in these 512 tokens the model will uh stray away from the Wikipedia entry but

中文：我们是不是要……所以让我直接按 进入后，有三种现存物种 等等，模型在这里生成了什么？ 完全复述了这一点。 维基百科条目正在背诵这段话 维基百科条目完全凭记忆撰写 该记忆存储在其参数中 因此，有可能在某个时候 在这 512 个代币中，模型将呃 不要参考维基百科条目，但

### 0:52:46–0:53:13

EN：you can see that it has huge chunks of it memorized here uh let me see for example if this sentence occurs by now okay so this so we're still on track let me check here okay we're still on track it will eventually uh stray away okay so this thing is just recited to a very large extent it will eventually deviate uh because it won't be able to remember exactly now the

中文：你可以看到它有大块的 它记住在这里了，嗯，让我看看。 例如这句话 现在已经发生了，好的，所以我们是 一切正常，让我确认一下 好的，我们还在继续。 追踪它最终会偏离轨道 好了，这段话就是背诵出来的。 在很大程度上，它将 最终会偏离，因为它不会 现在能够准确地记住

### 0:53:13–0:53:35

EN：reason that this happens is because these models can be extremely good at memorization and usually this is not what you want in the final model and this is something called regurgitation and it's usually undesirable to site uh things uh directly uh that you have trained on now the reason that this happens actually is because for a lot of documents like for example Wikipedia when these documents are deemed to be of

中文：造成这种情况的原因是： 这些模型可能非常擅长 记忆，而且通常这不是 您希望最终模型包含哪些内容？ 这叫做反刍。 而且通常不建议这样做。 直接来说，你拥有的东西 现在接受的训练，原因就在于此。 实际发生的情况是因为很多 例如维基百科之类的文档 当这些文件被认为是……

### 0:53:35–0:53:56

EN：very high quality as a source like for example Wikipedia it is very often uh the case that when you train the model you will preferentially sample from those sources so basically the model has probably done a few epochs on this data meaning that it has seen this web page like maybe probably 10 times or so and it's a bit like you like when you read some kind of a text many many times say

中文：质量非常高，例如作为来源 例如维基百科，它经常是呃 训练模型时遇到的情况 您将优先从以下来源取样 所以基本上该模型包含这些来源。 可能已经在这个数据集上进行了几个周期的训练。 这意味着它已经浏览过此网页 大概有十次左右吧 有点像你喜欢阅读的样子 某种文本多次提到

### 0:53:56–0:54:16

EN：you read something a 100 times uh then you'll be able to recite it and it's very similar for this model if it sees something way too often it's going to be able to recite it later from memory except these models can be a lot more efficient um like per presentation than human so probably it's only seen this Wikipedia entry 10 times but basically it has remembered this article exactly

中文：你把某件事读了100遍，呃…… 你将能够背诵它，而且它是 如果该模型检测到类似情况，则情况非常相似。 这种情况发生的频率实在太高了。 之后能够凭记忆复述出来 但这些模型可能远不止如此 高效的嗯，比如每次演示比 所以它可能只见过人类。 维基百科条目出现了10次，但基本上 它完全记住了这篇文章。

### 0:54:16–0:54:38

EN：in its parameters okay the next thing I want to show you is something that the model has definitely not seen during its training so for example if we go to the paper uh and then we navigate to the pre-training data we'll see here that uh the data set has a knowledge cut off until the end of 2023 so it will not have seen documents after this point and

中文：它的参数没问题，接下来我 想向你展示的是…… 该模型在其使用过程中绝对没有出现过。 训练，例如如果我们去…… 纸张，然后我们导航到 预训练数据我们在这里会看到，呃 数据集存在知识截止点 直到2023年底，所以不会 此后我看过一些文件，

### 0:54:38–0:55:01

EN：certainly it has not seen anything about the 2024 election and how it turned out now if we Prime the model with the tokens from the future it will continue the token sequence and it will just take its best guess according to the knowledge that it has in its own parameters so let's take a look at what that could look like so the Republican Party kit Trump okay president of the United

中文：当然，它肯定没有看到任何关于…… 2024年大选及其结果 现在，如果我们用以下方法启动模型： 来自未来的代币将继续 令牌序列，它只需要 这是根据……做出的最佳猜测 它自身所拥有的知识 参数，我们来看看它们是什么。 那看起来可能像 所以共和党工具包 特朗普，美国总统

### 0:55:01–0:55:26

EN：States from 2017 and let's see what it says after this point so for example the model will have to guess at the running mate and who it's against Etc so let's hit enter so here thingss that Mike Pence was the running mate instead of JD Vance and the ticket was against Hillary Clinton and Tim Kane so this is kind of a interesting parallel universe potentially of what could have happened

中文：来自各州 2017年，让我们看看之后会怎么说。 这一点，例如，该模型将 必须猜测竞选搭档是谁。 对手是谁等等，所以我们开始吧 所以，这里是迈克·彭斯的一些事情。 是他而不是JD Vance的竞选搭档 而这张竞选名单是针对希拉里的。 克林顿和蒂姆·凯恩，所以这有点…… 一个有趣的平行宇宙 可能发生的情况

### 0:55:26–0:55:49

EN：happened according to the LM let's get a different sample so the identical prompt and let's resample so here the running mate was Ronda santis and they ran against Joe Biden and Camala Harris so this is again a different parallel universe so the model will take educated guesses and it will continue the token sequence based on this knowledge um and it will just kind of like all of what we're seeing

中文：根据LM的说法，事情已经发生了，让我们来谈谈吧。 不同的样本，所以提示相同 好，我们开始吧。 重新采样，所以这里的竞选伙伴是 Ronda Santis和他们竞选乔 拜登和卡马拉·哈里斯，所以这又是 一个不同的平行宇宙，所以 模型会进行有根据的猜测，并且 将继续基于令牌序列 基于这些知识，嗯，它就会 就像我们看到的这一切一样。

### 0:55:49–0:56:12

EN：here is what's called hallucination the model is just taking its best guess uh in a probalistic manner the next thing I would like to show you is that even though this is a base model and not yet an assistant model it can still be utilized in Practical applications if you are clever with your prompt design so here's something that we would call a few shot prompt so what it is here is that I have

中文：这就是所谓的幻觉。 模型只是在做出它最好的猜测而已。 接下来，我以概率的方式…… 想向你们展示的是，即使 虽然这只是一个基础型号，而且尚未完全开发完成。 助理模特仍然可以是 在实际应用中使用 你的提示设计很巧妙 所以，这里有一种我们称之为……的东西 几张照片 所以，这里我要说的是，我有

### 0:56:12–0:56:37

EN：10 words or 10 pairs and each pair is a word of English column and then a the translation in Korean and we have 10 of them and what the model does here is at the end we have teacher column and then here's where we're going to do a completion of say just five tokens and these models have what we call in context learning abilities and what that's referring to is that as it is

中文：10 个单词或 10 对单词，每对单词都是一个 英文专栏，然后是 韩语翻译，我们有10个 它们以及该模型在这里所做的是 最后是教师专栏，然后 接下来我们要进行一项操作。 比如说，完成五个代币和 这些模型具有我们所说的在 情境学习能力以及什么 那指的是它本来的样子。

### 0:56:37–0:57:03

EN：reading this context it is learning sort of in place that there's some kind of a algorithmic pattern going on in my data and it knows to continue that pattern and this is called kind of like Inc context learning so it takes on the role of a translator and when we hit uh completion we see that the teacher translation is Sim which is correct um and so this is

中文：阅读此上下文，它正在学习排序。 在 某个地方存在某种 我的数据显示存在某种算法模式 它知道要继续这种模式 这有点像公司名称。 情境学习因此发挥了作用 的 翻译器，当我们达到完成状态时 我们看到教师的翻译是 Sim，没错，嗯，所以这是

### 0:57:03–0:57:24

EN：how you can build apps by being clever with your prompting even though we still just have a base model for now and it relies on what we call this um uh in context learning ability and it is done by constructing what's called a few shot prompt okay and finally I want to show you that there is a clever way to actually instantiate a whole language model assistant just by prompting and

中文：如何巧妙地构建应用程序 在你的提醒下，即使我们仍然 目前只有一个基础型号。 依赖于我们称之为“嗯嗯”的东西 具备情境学习能力，并且已经做到了。 通过构建所谓的少枪 提示：好的，最后我想展示一下 告诉你有一种巧妙的方法 实际上实例化一整套语言 只需提示即可成为模型助手

### 0:57:24–0:57:45

EN：the trick to it is that we're structure a prompt to look like a web page that is a conversation between a helpful AI assistant and a human and then the model will continue that conversation so actually to write the prompt I turned to chat gbt itself which is kind of meta but I told it I want to create an llm assistant but all I have is the base

中文：关键在于我们的结构 一个看起来像网页的提示 一段与乐于助人的人工智能的对话 助手、人类，然后是模型 我们将继续这个话题。 实际上，为了回答这个问题，我转向了 聊天本身就有点元 但我告诉它我想创建一个法学硕士 助手，但我只有基地

### 0:57:45–0:58:09

EN：model so can you please write my um uh prompt and this is what it came up with which is actually quite good so here's a conversation between an AI assistant and a human the AI assistant is knowledgeable helpful capable of answering wide variety of questions Etc and then here it's not enough to just give it a sort of description it works much better if you create this fot prompt so here's a

中文：所以，你能帮我写一下我的……嗯…… 提示音，这是它给出的结果。 实际上相当不错，所以这里是…… 人工智能助手与 人类 人工智能助手知识渊博 乐于助人，能够回答各种问题 各种各样的问题等等，然后这里 仅仅给它排序是不够的。 如果描述得更清楚一些，效果会好得多。 您创建了这个 fot 提示，所以这里有一个

### 0:58:10–0:58:37

EN：few terms of human assistant human assistant and we have uh you know a few turns of conversation and then here at the end is we're going to be putting the actual query that we like so let me copy paste this into the base model prompt and now let me do human column and this is where we put our actual prompt why is the sky blue and uh let's uh

中文：人类助手的几个术语 助理，我们还有一些…… 谈话几番之后，就到了这里 最后，我们要把 我们喜欢的实际查询，让我复制一下。 将此内容粘贴到基础模型提示符中 现在让我来写一篇关于人物专栏的文章。 这是我们放置实际提示“为什么”的地方 天空 蓝色，呃，我们呃

### 0:58:37–0:58:58

EN：run assistant the sky appears blue due to the phenomenon called R lights scattering etc etc so you see that the base model is just continuing the sequence but because the sequence looks like this conversation it takes on that role but it is a little subtle because here it just uh you know it ends the assistant and then just you know hallucinate Ates the next question by the human Etc so it'll just continue

中文：运行助手，天空看起来是蓝色的 被称为R光现象 散射等等，所以你可以看到 基础模型只是延续了 序列，但因为序列看起来 就像这场对话一样，它呈现出来的样子 扮演这个角色，但有点微妙，因为 就到此为止了，你知道的。 助理，然后你就知道了 幻觉阿特斯提出了下一个问题 人类等等，所以它会继续下去。

### 0:58:58–0:59:16

EN：going on and on uh but you can see that we have sort of accomplished the task and if you just took this why is the sky blue and if we just refresh this and put it here then of course we don't expect this to work with a base model right we're just going to who knows what we're going to get okay we're just going to get more

中文：一直持续下去，呃，但是你可以看到 我们基本上已经完成了这项任务。 如果你只是接受了这一点，那么天空为什么是这样的呢？ 蓝色，如果我们刷新一下并放入 那么它就在这里，我们当然不会指望它在这里。 这样才能与基础模型配合使用，对吧？ 我们只是要去谁也不知道我们要去哪里 没事的，我们这就去 了解更多

### 0:59:16–0:59:42

EN：questions okay so this is one way to create an assistant even though you may only have a base model okay so this is the kind of brief summary of the things we talked about over the last few minutes now let me zoom out here and this is kind of like what we've talked about so far we wish to train LM assistants like chpt we've discussed the first stage of that which is the

中文：问题好的，这是其中一种方法 即使你可能……也要创建一个助手 只有基本型号，好的，就是这样。 对事物的简要概述 我们过去几周一直在讨论这个问题 现在几分钟了，让我把镜头拉远。 这里，这有点像我们…… 到目前为止，我们希望训练LM。 像 chpt 这样的助手，我们已经讨论过了 第一阶段，即

## 9. pretraining to post-training（0:59:23–1:01:06）

### 0:59:42–1:00:05

EN：pre-training stage and we saw that really what it comes down to is we take Internet documents we break them up into these tokens these atoms of little text chunks and then we predict token sequences using neural networks the output of this entire stage is this base model it is the setting of The parameters of this network and this base model is basically an internet document simulator on the token level so it can

中文：训练前阶段，我们看到 归根结底，我们采取 我们将互联网文档分解成 这些标记，这些微小的文本原子 先将数据块分割成块，然后预测词元。 使用神经网络的序列 整个阶段的输出就是这个基础部分。 模型是它的设置 该网络的参数 模型本质上是一个网络文档 在令牌级别上进行模拟器，以便它可以

### 1:00:05–1:00:23

EN：just uh it can generate token sequences that have the same kind of like statistics as Internet documents and we saw that we can use it in some applications but we actually need to do better we want an assistant we want to be able to ask questions and we want the model to give us answers and so we need to now go into the second stage which is

中文：它可以生成令牌序列 具有相同类型 统计数据作为互联网文档，我们 发现我们可以在某些方面使用它 应用程序，但我们实际上需要做 我们更想要一个助理，我们想要 能够提问，我们希望 我们需要一个模型来给我们提供答案，所以我们需要它。 现在进入第二阶段，即

### 1:00:23–1:00:47

EN：called the post-training stage so we take our base model our internet document simulator and hand it off to post training so we're now going to discuss a few ways to do what's called post training of these models these stages in post training are going to be computationally much less expensive most of the computational work all of the massive data centers um and all of the sort of heavy compute and millions of

中文：称为训练后阶段，所以我们 以我们的基础模型——互联网为例 文档模拟器并将其移交给 训练结束后，我们现在要…… 讨论几种实现所谓“实现”的方法 这些模型的训练之后 培训后的各个阶段将是： 计算成本要低得多 计算工作全部 大型数据中心以及所有 某种重型计算和数百万

### 1:00:47–1:01:10

EN：dollars are the pre-training stage but now we go into the slightly cheaper but still extremely important stage called post trining where we turn this llm model into an assistant so let's take a look at how we can get our model to not sample internet documents but to give answers to questions so in other words what we want to do is we want to start thinking about conversations and these

中文：美元是预备训练阶段，但 现在我们来看看稍微便宜一些的，但是 仍然极其重要的阶段，称为 培训结束后，我们将转向这个LLM 把模特转型成助理，我们来看一个例子。 看看我们如何才能让我们的模型不 示例互联网文档，但要给出 换句话说，就是问题的答案 我们想做的就是开始 思考对话和这些

## 10. post-training data (conversations)（1:01:06–1:20:32）

### 1:01:10–1:01:29

EN：are conversations that can be multi-turn so so uh there can be multiple turns and they are in the simplest case a conversation between a human and an assistant and so for example we can imagine the conversation could look something like this when a human says what is 2 plus2 the assistant should re respond with something like 2 plus 2 is 4 when a human follows up and says what

中文：是可以进行多轮的对话。 所以，呃，可能会有多轮。 最简单的情况下，它们是…… 人与人之间的对话 助手，例如我们可以 想象一下对话可能会是这样的 当一个人说类似这样的话 2加2等于多少？助手应该重新回答 回答类似“2加2等于多少”这样的问题。 4 当有人跟进并说……

### 1:01:29–1:01:48

EN：if it was star instead of a plus assistant could respond with something like this um and similar here this is another example showing that the assistant could also have some kind of a personality here uh that it's kind of like nice and then here in the third example I'm showing that when a human is asking for something that we uh don't wish to help with we can produce what's called

中文：如果是星号而不是加号的话。 助手可能会回复一些内容 喜欢 这个，嗯，这里也类似，这是另一个 例如，助理可以 也具有某种个性。 这里感觉还不错， 那么，在第三个例子中，我是 这表明当人类提出要求时 我们不想帮忙。 有了它，我们就可以生产出所谓的

### 1:01:48–1:02:08

EN：refusal we can say that we cannot help with that so in other words what we want to do now is we want to think through how in a system should interact with the human and we want to program the assistant and Its Behavior in these conversations now because this is neural networks we're not going to be programming these explicitly in code we're not going to be able to program

中文：拒绝的话，我们可以说我们无能为力。 换句话说，我们想要的是什么？ 现在我们要做的就是仔细思考。 系统中应该如何与 人类，我们想对人类进行编程。 助手及其在这些方面的行为 现在进行对话是因为这是神经性的 我们不会是网络 这些操作需要在代码中明确地编程实现。 我们将无法进行编程。

### 1:02:08–1:02:30

EN：the assistant in that way because this is neural networks everything is done through neural network training on data sets and so because of that we are going to be implicitly programming the assistant by creating data sets of conversations so these are three independent examples of conversations in a data dat set an actual data set and I'm going to show you examples will be much larger it could have hundreds of

中文：以这种方式担任助理，因为这样 神经网络就万事大吉了。 通过对数据进行神经网络训练 集合，因此，我们要去 隐式地进行编程 助手通过创建数据集 对话共有三段。 对话中的独立例子 数据数据集，实际数据集和 我将向你们展示一些例子。 体积要大得多，可能有数百个。

### 1:02:31–1:02:54

EN：thousands of conversations that are multi- turn very long Etc and would cover a diverse breath of topics but here I'm only showing three examples but the way this works basically is uh a assistant is being programmed by example and where is this data coming from like 2 * 2al 4 same as 2 plus 2 Etc where does that come from this comes from Human labelers so we will basically give

中文：成千上万的对话 多圈很长等等，而且会 涵盖广泛的主题，但 这里我只举三个例子，但是 它的运作方式基本上是这样的…… 助手正在通过示例进行编程。 这些数据来自哪里？ 2 * 2al 4 等同于 2 加 2 等等，其中 那是不是来自这里？ 人工标注员，所以我们基本上会给出

### 1:02:54–1:03:17

EN：human labelers some conversational context and we will ask them to um basically give the ideal assistant response in this situation and a human will write out the ideal response for an assistant in any situation and then we're going to get the model to basically train on this and to imitate those kinds of responses so the way this works then is we are going to take our base model

中文：人工标注员的一些对话 我们会询问他们相关背景，并要求他们…… 基本上就是提供理想的助手 在这种情况下，人类的反应 将写出理想的回应 在任何情况下担任助手 我们将把模型弄到 基本上就是以此为目标进行训练和模仿。 那种类型的 所以，它的运作方式是这样的： 我们将采用我们的基础模型

### 1:03:17–1:03:37

EN：which we produced in the preing stage and this base model was trained on internet documents we're now going to take that data set of internet documents and we're gonna throw it out and we're going to substitute a new data set and that's going to be a data set of conversations and we're going to continue training the model on these conversations on this new data set of conversations and what happens is that

中文：我们在预生产阶段生产的 该基础模型是在 我们现在要访问的互联网文档 取该互联网文档数据集 我们要把它扔掉，我们是 将替换为新的数据集 那将是一个数据集 对话，我们将要 继续用这些数据训练模型。 关于这一新数据集的讨论 对话的内容和结果如下：

### 1:03:37–1:04:01

EN：the model will very rapidly adjust and will sort of like learn the statistics of how this assistant responds to human queries and then later during inference we'll be able to basically um Prime the assistant and get the response and it will be imitating what the humans will human labelers would do in that situation if that makes sense so we're going to see examples of that and this

中文：该模型将很快进行调整， 有点像学习统计学 该助手如何回应人类 查询，然后在推理过程中。 我们基本上可以……嗯……Prime 协助并获取回复，然后它 将会模仿人类的行为 人工标注员会这样做。 如果这样说你能理解的话，情况就是这样。 去看看这方面的例子，还有这个

### 1:04:01–1:04:23

EN：is going to become bit more concrete I also wanted to mention that this post-training stage we're going to basically just continue training the model but um the pre-training stage can in practice take roughly three months of training on many thousands of computers the post-training stage will typically be much shorter like 3 hours for example um and that's because the data set of conversations that we're going to create

中文：将会变得更加具体一些。 还想提一下这一点 训练后阶段，我们将…… 基本上就是继续训练。 模型，但是预训练阶段可以 实际上大约需要三个月的时间 在数以千计的计算机上进行训练 训练后阶段通常会 时间可以短得多，比如 3 小时。 嗯，那是因为数据集 我们将要展开的对话

### 1:04:23–1:04:46

EN：here manually is much much smaller than the data set of text on the internet and so this training will be very short but fundamentally we're just going to take our base model we're going to continue training using the exact same algorithm the exact same everything except we're swapping out the data set for conversations so the questions now are what are these conversations how do we represent them how do we get the model

中文：这里手动操作比 互联网上的文本数据集和 所以这次培训会很短，但是 从根本上讲，我们只是要采取 我们将继续沿用我们的基本模式。 使用完全相同的算法进行训练 除了我们是之外，其他一切都一模一样。 替换数据集 对话，所以现在的问题是： 这些对话是什么？我们如何进行这些对话？ 如何表示它们，我们如何获得模型

### 1:04:46–1:05:08

EN：to see conversations instead of just raw text and then what are the outcomes of um this kind of training and what do you get in a certain like psychological sense uh when we talk about the model so let's turn to those questions now so let's start by talking about the tokenization of conversations everything in these models has to be turned into tokens because everything is just about

中文：看到的是对话，而不仅仅是原始数据。 文本以及结果是什么？ 嗯，这种训练，你觉得怎么样？ 进入某种类似心理状态 感觉，呃，当我们谈论模型的时候，所以 现在让我们来讨论这些问题吧。 我们先来谈谈…… 对话标记化一切 在这些模型中，必须转化为 因为一切都与代币有关

### 1:05:08–1:05:29

EN：token sequences so how do we turn conversations into token sequences is the question and so for that we need to design some kind of ending coding and uh this is kind of similar to maybe if you're familiar you don't have to be with for example the TCP IP packet in um on the internet there are precise rules and protocols for how you represent information how everything is structured

中文：那么，我们如何转换标记序列呢？ 将对话转换成标记序列是 这个问题，因此我们需要…… 设计某种结尾编码，呃…… 这有点像……如果 你熟悉就好，你不必非得是 例如，以微米为单位的 TCP/IP 数据包。 互联网上有明确的规则。 以及您如何代表的协议 信息如何组织一切

### 1:05:29–1:05:48

EN：together so that you have all this kind of data laid out in a way that is written out on a paper and that everyone can agree on and so it's the same thing now happening in llms we need some kind of data structures and we need to have some rules around how these data structures like conversations get encoded and decoded to and from tokens and so I want to show you now how I

中文：放在一起，这样你就拥有了所有这些种类 数据以一种如下方式呈现： 写在纸上，而且每个人都 可以达成共识，所以它们是一样的。 现在在LLMS中发生的事情，我们需要某种 数据结构，我们需要有 关于这些数据的一些规则 像对话这样的结构会变得 编码和解码为令牌，以及从令牌编码和解码。 所以现在我想向你们展示我是如何做到的。

### 1:05:48–1:06:13

EN：would recreate uh this conversation in the token space so if you go to Tech tokenizer I can take that conversation and this is how it is represented in uh for the language model so here we have we are iterating a user and an assistant in this two- turn conversation and what you're seeing here is it looks ugly but it's actually relatively simple the way it gets turned

中文：会 重现这段对话 代币空间，所以如果你去科技 分词器 我可以接受这样的对话，而这…… 它在呃中是如何表示的 语言模型，所以我们在这里有 在迭代过程中，用户和助手 这两轮 对话以及你在这里看到的内容 它看起来很丑，但实际上 它的转动方式相对简单

### 1:06:13–1:06:36

EN：into a token sequence here at the end is a little bit complicated but at the end this conversation between a user and assistant ends up being 49 tokens it is a one-dimensional sequence of 49 tokens and these are the tokens okay and all the different llms will have a slightly different format or protocols and it's a little bit of a wild west right now but for example GPT

中文：最后这里变成了一个标记序列。 有点复杂，但最后…… 用户与 助手最终需要 49 个代币。 一个包含 49 个标记的一维序列 这些就是代币。 好的，所有不同的LLM都会 格式略有不同或 协议，而且有点像 现在的情况就像狂野西部，但例如GPT

### 1:06:36–1:07:02

EN：40 does it in the following way you have this special token called imore start and this is short for IM imaginary monologue uh the start then you have to specify um I don't actually know why it's called that to be honest then you have to specify whose turn it is so for example user which is a token 4 28 then you have internal monologue separator and then it's the exact

中文：40 是通过以下方式实现的：你有 这个名为 imore start 的特殊代币 这是 IM imaginary 的缩写。 独白呃 首先，你必须具体说明，嗯，我 我其实不知道它为什么叫这个名字。 说实话，那你必须具体说明。 轮到谁了？例如用户 这是一个令牌 4 28 然后你就会陷入内心独白 分隔符，然后就是精确的

### 1:07:03–1:07:27

EN：question so the tokens of the question and then you have to close it so I am end the end of the imaginary monologue so basically the question from a user of what is 2 plus two ends up being the token sequence of these tokens and now the important thing to mention here is that IM start this is not text right IM start is a special token that gets added

中文：问题，所以问题的标记 然后你必须把它关掉，所以我是 结束这段想象中的独白 所以 基本上，这是来自一位用户的问题 2加2等于多少？ 这些标记的标记序列，现在 这里需要特别指出的是： 那条即时消息开始，这不是文本对吧？ 开始是一个特殊的标记，会被添加进去。

### 1:07:27–1:07:49

EN：it's a new token and um this token has never been trained on so far it is a new token that we create in a post-training stage and we introduce and so these special tokens like IM seep IM start Etc are introduced and interspersed with text so that they sort of um get the model to learn that hey this is a the start of a turn for who is it start of

中文：这是一个新代币，嗯，这个代币有 目前为止还没有接受过这方面的培训，这是一个新的。 我们在训练后创建的令牌 舞台，我们介绍，以及这些 特殊代币，例如 IM 渗漏 IM 开始等等 引入并穿插着 发短信让他们大概明白 模型学习到，嘿，这是一个 回合开始，是谁的开始？

### 1:07:49–1:08:09

EN：the turn for the start of the turn is for the user and then this is what the user says and then the user ends and then it's a new start of a turn and it is by the assistant and then what does the assistant say well these are the tokens of what the assistant says Etc and so this conversation is not turned into the sequence of tokens the specific

中文：回合开始的回合是 对于用户而言，这就是…… 用户说完后，用户结束了对话。 然后，一切又重新开始，进入一个新的阶段。 由助理负责，然后呢？ 助理说，这些是 助理所说的话的凭证等等 因此，这场对话并没有结束。 将特定标记序列

### 1:08:09–1:08:33

EN：details here are not actually that important all I'm trying to show you in concrete terms is that our conversations which we think of as kind of like a structured object end up being turned via some encoding into onedimensional sequences of tokens and so because this is one dimensional sequence of tokens we can apply all the stuff that we applied before now it's just a sequence of tokens and now we can train a language

中文：这里的细节其实并非如此。 重要的是，我试图向你展示的一切 具体来说，就是我们的对话。 我们认为这有点像…… 结构化对象最终会被翻转 通过某种编码方式变成一维的 标记序列，因此因为这个 是一个一维的标记序列，我们 可以应用我们应用的所有东西。 在此之前，它只是一系列的 现在我们可以训练一种语言了，有了标记，我们就可以训练语言了。

### 1:08:33–1:08:55

EN：model on it and so we're just predicting the next token in a sequence uh just like before and um we can represent and train on conversations and then what does it look like at test time during inference so say we've trained a model and we've trained a model on these kinds of data sets of conversations and now we want to inference so during inference what does this look like when you're on on chash

中文：基于此模型，我们只是在进行预测。 序列中的下一个标记，呃，就是 就像以前一样，我们可以代表…… 进行对话训练，然后呢？ 看起来像是在测试期间 推理，假设我们已经训练了一个模型 我们已经针对这些类型训练了一个模型。 对话数据集，现在我们 想要 那么在推理过程中，什么会起作用呢？ 这看起来就像你在玩 Chash 游戏一样

### 1:08:55–1:09:17

EN：apt well you come to chash apt and you have say like a dialogue with it and the way this works is basically um say that this was already filled in so like what is 2 plus 2 2 plus 2 is four and now you issue what if it was times I am end and what basically ends up happening um on the servers of open AI or something like that is they

中文：apt well 你来到 chash apt，然后你 可以像对话一样和它交流。 这种方式的运作原理是 基本上，嗯，可以说这已经是…… 填好后，比如 2 加 2 等于多少？ 加 2 等于 4，现在你问：如果 那是我结束的时候，基本上就是这样。 最终发生在服务器上 开放人工智能之类的组织就是他们

### 1:09:18–1:09:38

EN：put in I start assistant I amep and this is where they end it right here so they construct this context and now they start sampling from the model so it's at this stage that they will go to the model and say okay what is a good for sequence what is a good first token what is a good second token what is a good third token and this is where the LM

中文：放入我启动助手我amep和这个 这就是他们故事的结尾，所以他们 构建了这个背景，现在他们 开始从模型中采样，使其处于 他们将进入的这个阶段 模型并说，好的，什么对……有好处 序列中，一个好的第一个标记是什么？ 好的第二个代币是什么？好的 第三个令牌，也是LM所在的地方。

### 1:09:38–1:10:01

EN：takes over and creates a response like for example response that looks something like this but it doesn't have to be identical to this but it will have the flavor of this if this kind of a conversation was in the data set so um that's roughly how the protocol Works although the details of this protocol are not important so again my goal is that just to show you that everything

中文：接管并产生类似这样的响应 例如，这样的响应 类似这样的东西，但它没有 与此相同，但它将有 这种味道如果是这种类型的 对话内容包含在数据集中，所以…… 协议的工作原理大致就是这样。 尽管该协议的细节尚不清楚 这些都不重要，所以我的目标是 只是想向你展示这一切

### 1:10:01–1:10:23

EN：ends up being just a one-dimensional token sequence so we can apply everything we've already seen but we're now training on conversations and we're now uh basically generating conversations as well okay so now I would like to turn to what these data sets look like in practice the first paper that I would like to show you and the first effort in this direction is this paper from openai in 2022 and this

中文：最终却变成了一个一维的 令牌序列，以便我们可以应用 我们已经看到的一切，但是我们 现在正在进行对话训练，我们正在 现在基本上是在生成 对话也很好，所以现在我 我们想看看这些数据是什么。 实际上，集合看起来像第一组 我想给你们看看这份文件。 朝这个方向迈出的第一步是 这篇来自 OpenAI 2022 年的论文以及这篇

### 1:10:23–1:10:41

EN：paper was called instruct GPT or the technique that they developed and this was the first time that opena has kind of talked about how you can take language models and fine-tune them on conversations and so this paper has a number of details that I would like to take you through so the first stop I would like to make is in section 3.4 where they talk about the human

中文：这篇论文被称为指导 GPT 或 他们开发的技术以及这项技术 这是 Opena 第一次有这种 谈到了如何采取 语言模型并对其进行微调 对话，因此本文有 我想了解的细节有很多 带你参观，所以第一站我 想在 3.4 节中说明。 他们在那里谈论人类

### 1:10:41–1:11:06

EN：contractors that they hired uh in this case from upwork or through scale AI to uh construct these conversations and so there are human labelers involved whose job it is professionally to create these conversations and these labelers are asked to come up with prompts and then they are asked to also complete the ideal assistant responses and so these are the kinds of prompts that people came up with so these are human labelers

中文：他们雇佣的承包商，呃，在这个 案例来自 Upwork 或通过 Scale AI 呃，构建这些对话等等 其中有人工标注员参与， 这项工作的专业性在于创造这些 对话和这些标签是 被要求想出一些提示语，然后 他们还被要求完成以下事项： 理想的助手回应以及这些 这些都是人们会提出的提示。 所以，这些是人工标签员。

### 1:11:06–1:11:27

EN：so list five ideas for how to regain enthusiasm for my career what are the top 10 science fiction books I should read next and there's many different types of uh kind of prompts here so translate this sentence from uh to Spanish Etc and so there's many things here that people came up with they first come up with the prompt and then they also uh answer that prompt and they give

中文：请列出五条恢复的方法。 我对我的事业充满热情，具体是什么？ 我应该读的十大科幻小说 接下来请阅读，有很多不同的内容。 这里有一些提示类型。 把这句话从“呃”翻译成 西班牙语等等，还有很多其他东西。 这里是人们最初提出的想法。 想出提示，然后他们 还有，呃，回答那个提示，他们会给你

### 1:11:28–1:11:49

EN：the ideal assistant response now how do they know what is the ideal assistant response that they should write for these prompts so when we scroll down a little bit further we see that here we have this excerpt of labeling instructions uh that are given to the human labelers so the company that is developing the language model like for example open AI writes up labeling instructions for how the humans should

中文：现在理想的助手应该如何回应？ 他们知道理想的助手是什么样的。 他们应该写什么样的回应？ 这些提示会在我们向下滚动时出现。 再往前走一点，我们看到这里我们 以下是标签摘录 给……的指示 人工标签员，所以这家公司是 开发语言模型，例如 例如，OpenAI撰写的标注报告 人类应该如何行事的指南

### 1:11:49–1:12:10

EN：create ideal responses and so here for example is an excerpt uh of these kinds of labeling instruction instructions on High level you're asking people to be helpful truthful and harmless and you can pause the video if you'd like to see more here but on a high level basically just just answer try to be helpful try to be truthful and don't answer questions that we don't want um kind of

中文：创建理想的回应，因此在这里 例如，这是这类内容的摘录。 标签说明说明 你要求人们达到很高的水平。 乐于助人、诚实无害，而且你 如果您想观看，可以暂停视频。 更多内容请点击此处，但总体而言 尽量回答，希望能帮到你。 实话实说，不要回答 我们不想问的问题，嗯……

### 1:12:10–1:12:34

EN：the system to handle uh later in chat gbt and so roughly speaking the company comes up with the labeling instructions usually they are not this short usually there are hundreds of pages and people have to study them professionally and then they write out the ideal assistant responses uh following those labeling instructions so this is a very human heavy process as it was described in this paper now the data set for instruct

中文：稍后在聊天中处理这个问题的系统 gbt，所以粗略地说，这家公司 制定标签说明 通常它们不会这么短 有数百页内容和数百人 必须对其进行专业研究，并且 然后他们写出了理想的助理人选。 随后的回复 说明，所以这非常人性化。 正如文中所描述的那样，这是一个繁重的过程。 本文现在提供了用于指导的数据集

### 1:12:34–1:12:56

EN：GPT was never actually released by openi but we do have some open- Source um reproductions that were're trying to follow this kind of a setup and collect their own data so one that I'm familiar with for example is the effort of open Assistant from a while back and this is just one of I think many examples but I just want to show you an example so here's so these were people on the

中文：GPT 实际上从未被 openi 发布过。 但我们确实有一些开源的…… 那些试图复制的东西 按照这种设置进行收集 他们自己的数据，所以我很熟悉这些数据。 例如，开放的努力就是如此。 这是之前一位助理的作品。 这只是众多例子中的一个，但我 只是想给你举个例子而已。 所以这些人当时在……

### 1:12:56–1:13:18

EN：internet that were asked to basically create these conversations similar to what um open I did with human labelers and so here's an entry of a person who came up with this BR can you write a short introduction to the relevance of the term manop uh in economics please use examples Etc and then the same person or potentially a different person will write up the response so here's the

中文：互联网基本上被要求 创建类似这样的对话 我和人工标签员一起做的公开工作是什么？ 所以，这里是一位人士的条目： 我想出了这个BR，你能写一个吗？ 简要介绍其相关性 期限 经济学中的 manop uh 请用 例如等等，然后是同一个人或 或许是另一个人 请写下回复，内容如下：

### 1:13:18–1:13:45

EN：assistant response to this and so then the same person or different person will actually write out this ideal response and then this is an example of maybe how the conversation could continue now explain it to a dog and then you can try to come up with a slightly a simpler explanation or something like that now this then becomes the label and we end up training on this so what happens during training

中文：助理对此的回应，以及随后的情况。 同一个人或不同的人会 实际上，把这个理想状态写下来。 回应，然后这是一个例子 或许对话可以这样进行 现在继续，把它解释给狗听。 然后你可以试着想出一个 稍微简单一点的解释或 现在大概就是这样。 标签就此诞生，最终我们接受了培训。 那么，训练期间会发生什么呢？

### 1:13:45–1:14:09

EN：is that um of course we're not going to have a full coverage of all the possible questions that um the model will encounter at test time during inference we can't possibly cover all the possible prompts that people are going to be asking in the future but if we have a like a data set of a few of these examples then the model during training will start to take on this Persona of

中文：当然，我们不会…… 全面覆盖所有可能的情况 模型将提出的问题 在推理测试期间遇到这种情况 我们不可能涵盖所有可能的情况。 提示人们将会 以后再问，但如果我们有 就像包含其中一些数据的数据集一样 例如，然后是训练过程中的模型 将开始扮演这个角色

### 1:14:09–1:14:32

EN：this helpful truthful harmless assistant and it's all programmed by example and so these are all examples of behavior and if you have conversations of these example behaviors and you have enough of them like 100,00 and you train on it the model sort of starts to understand the statistical pattern and it kind of takes on this personality of this assistant now it's possible that when you get the exact same question like

中文：这位乐于助人、诚实无害的助手 所有这些都是通过示例编程实现的。 以上这些都是行为的例子。 如果你谈论这些话题 例如行为，你就有足够的了 它们就像100,000，你用它们进行训练。 模型似乎开始理解 统计模式，而且它需要一些时间 就这种性格而言 现在助理有可能在 你会收到完全相同的问题，例如

### 1:14:32–1:14:58

EN：this at test time it's possible that the answer will be recited as exactly what was in the training set but more likely than that is that the model will kind of like do something of a similar Vibe um and we will understand that this is the kind of answer that you want um so that's what we're doing we're programming the system um by example and the system adopts statistically this

中文：在测试阶段，有可能出现这种情况 答案将如实复述。 曾在训练集中出现，但更有可能 也就是说，该模型会有点…… 比如做一些类似氛围的事情 我们将明白这是 你想要的那种答案，嗯…… 这就是我们正在做的。 通过示例对系统进行编程 该系统从统计学角度采用了这种方法。

### 1:14:58–1:15:19

EN：Persona of this helpful truthful harmless assistant which is kind of like reflected in the labeling instructions that the company creates now I want to show you that the state-of-the-art has kind of advanced in the last 2 or 3 years uh since the instr GPT paper so in particular it's not very common for humans to be doing all the heavy lifting just by themselves anymore and that's because we now have language models and

中文：这位乐于助人、诚实的人格 无害的助手，有点像 标签说明中有所体现 该公司现在创造的，我想 向您展示最先进的技术已经 最近两三年发展得比较好。 自从GPT论文发表以来已经过去好几年了。 具体来说，这种情况并不常见。 让人类承担所有重体力劳动 他们不再孤身一人了，就是这样。 因为我们现在有了语言模型，

### 1:15:19–1:15:37

EN：these language models are helping us create these data sets and conversations so it is very rare that the people will like literally just write out the response from scratch it is a lot more likely that they will use an existing llm to basically like uh come up with an answer and then they will edit it or things like that so there's many different ways in which now llms have

中文：这些语言模型对我们很有帮助。 创建这些数据集和对话 所以人们很少会 就像直接把……写出来一样 从头开始响应要复杂得多。 他们很可能会使用现有的 llm 基本上就像是……想出一个 回答后，他们会进行编辑。 诸如此类的事情有很多。 现在 llms 有的不同方式

### 1:15:37–1:16:01

EN：started to kind of permeate this posttraining Set uh stack and llms are basically used pervasively to help create these massive data sets of conversations so I don't want to show like Ultra chat is one um such example of like a more modern data set of conversations it is to a very large extent synthetic but uh I believe there's some human involvement I could be wrong with that usually there will be

中文：开始逐渐渗透到这个领域。 训练后设置 uh 堆栈和 llms 是 基本上广泛用于帮助 创建这些庞大的数据集 对话，所以我不想展示 比如 Ultra Chat 就是一个例子。 就像一个更现代的数据集 对话涉及范围非常广。 合成程度，但呃，我相信 这里面涉及到一些人为因素，我可以…… 这样做通常会出错。

### 1:16:01–1:16:21

EN：a little bit of human but there will be a huge amount of synthetic help um and this is all kind of like uh constructed in different ways and Ultra chat is just one example of many sft data sets that currently exist and the only thing I want to show you is that uh these data sets have now millions of conversations uh these conversations are mostly synthetic but they're probably edited to

中文：多少有人性，但会有的 大量的合成帮助，嗯， 这一切都像是人为构建的。 以不同的方式，而 Ultra 聊天只是 众多SFT数据集中的一个例子是 目前存在，而且我唯一拥有的 想向你们展示的是这些数据 现在，对话集已包含数百万条对话。 呃，这些对话大多是 合成的，但它们可能经过编辑

### 1:16:21–1:16:46

EN：some extent by humans and they span a huge diversity of sort of um uh areas and so on so these are fairly extensive artifacts by now and there's all these like sft mixtures as they're called so you have a mixture of like lots of different types and sources and it's partially synthetic partially human and it's kind of like um gone in that direction since uh but roughly

中文：在某种程度上，人类也参与其中，它们跨越了…… 种类繁多 嗯，呃，区域等等，所以这些都是 目前已收集到相当多的文物。 有各种各样的类似SFT的混合物 它们被称为……所以你有一个混合物 像很多不同类型和来源 而且它是部分合成的 人类，而且有点像……消失了 朝那个方向，嗯，但大致如此。

### 1:16:46–1:17:10

EN：speaking we still have sft data sets they're made up of conversations we're training on them um just like we did before and uh I guess like the last thing to note is that I want to dispel a little bit of the magic of talking to an AI like when you go to chat GPT and you give it a question and then you hit enter uh what is coming back is kind of like

中文：也就是说，我们仍然拥有 sft 数据集 它们由我们的对话组成 就像我们之前做的那样，对他们进行训练。 之前和 呃，我想最后一点需要注意的是…… 我想澄清一点…… 与人工智能对话的魔力就像…… 你去聊天 GPT，然后你给它一个 问完问题后，你按回车键，呃，什么？ 回归有点像

### 1:17:10–1:17:36

EN：statistically aligned with what's happening in the training set and these training sets I mean they really just have a seed in humans following labeling instructions so what are you actually talking to in chat GPT or how should you think about it well it's not coming from some magical AI like roughly speaking it's coming from something that is statistically imitating human labelers which comes from labeling instructions written by these companies and so you're

中文：统计上与以下情况一致 训练集中发生的这些 训练组我的意思是，它们真的只是 人类在贴标签后会有种子。 指示，所以你到底是什么？ 在聊天中与 GPT 交谈，或者你应该怎么做？ 仔细想想，它并非来自…… 某种神奇的人工智能，粗略地说 它来自某个地方 统计上模仿人类标签者 这是从标签说明中得出的结论。 由这些公司编写，所以你

### 1:17:36–1:18:00

EN：kind of imitating this uh you're kind of getting um it's almost as if you're asking human labeler and imagine that the answer that is given to you uh from chbt is some kind of a simulation of a human labeler uh and it's kind of like asking what would a human labeler say in this kind of a conversation and uh it's not just like this human labeler is not just like a random person

中文：有点像在模仿这个，呃，你有点像 感觉就像你 询问人工标注员并想象一下 给你的答案来自 chbt 是一种模拟 人工贴标签员，嗯，有点像…… 问：如果由人类标注员来标注，他们会怎么说？ 这种对话 而且，这不仅仅像这个人一样 标签制作者并非普通人。

### 1:18:00–1:18:21

EN：from the internet because these companies actually hire experts so for example when you are asking questions about code and so on the human labelers that would be in um involved in creation of these conversation data sets they will usually be usually be educated expert people and you're kind of like asking a question of like a simulation of those people if that makes sense so you're not talking to a magical AI

中文：来自互联网，因为这些 公司实际上会聘请专家来…… 例如，当你提问时 关于代码等等，人工标注员 那将与创造有关。 这些对话数据集 通常情况下，他们会接受教育。 专家们，你有点像…… 提出类似模拟的问题 如果这样说你能理解的话，这些人就是如此。 你不是在和魔法人工智能对话。

### 1:18:21–1:18:42

EN：you're talking to an average labeler this average labeler is probably fairly highly skilled but you're talking to kind of like an instantaneous simulation of that kind of a person that would be hired uh in the construction of these data sets so let me give you one more specific example before we move on for example when I go to chpt and I say recommend the top five landmarks who see in Paris and then I

中文：你正在和一个普通的标签制作商交谈。 这位平均水平的标签员可能相当 高技能 但你现在说话的方式有点像是在跟…… 那种情况的瞬时模拟 会被雇佣的人 构建这些数据集，所以让我们 我再举一个具体的例子。 例如，在我们继续之前，当我…… 到 chpt，我推荐前五名 在巴黎看到的那些地标，然后我

### 1:18:42–1:18:49

EN：hit enter

中文：打 进入

### 1:18:52–1:19:13

EN：uh okay here we go okay when I hit enter what's coming out here how do I think about it well it's not some kind of a magical AI that has gone out and researched all the landmarks and then ranked them using its infinite intelligence Etc what I'm getting is a statistical simulation of a labeler that was hired by open AI you can think about it roughly in that way and so if this

中文：嗯，好的，开始了，当我按下回车键时 这里到底发生了什么？我怎么看？ 关于这件事，嗯，它并不是某种…… 神奇的人工智能已经出去了 研究了所有地标，然后 使用其无限的排名对它们进行排名 情报等等，我得到的是 对标签器进行统计模拟 受聘于 OpenAI，你可以考虑一下 大致就是这样，所以如果这样

### 1:19:13–1:19:32

EN：specific um question is in the posttraining data set somewhere at open aai then I'm very likely to see an answer that is probably very very similar to what that human labeler would have put down for those five landmarks how does the human labeler come up with this well they go off and they go on the internet and they kind of do their own little research for 20 minutes and they just

中文：具体问题在…… 训练后数据集位于某个开放位置 如果是这样，那我很有可能会看到一个 答案很可能非常非常 这与人工标注员的做法类似。 已经放下 对于这五个地标，它们是如何运作的？ 人工标注员想出了这个好主意 他们离开，然后上网。 他们有点像是在做自己的小事。 他们研究了20分钟，然后就……

### 1:19:32–1:19:53

EN：come up with a list right now so if they come up with this list and this is in the data set I'm probably very likely to see what they submitted as the correct answer from the assistant now if this specific query is not part of the post training data set then what I'm getting here is a little bit more emergent uh because uh the model kind of understands

中文：现在就列个清单，这样如果他们 列出这份清单，这其中就包括 我很有可能会得到的数据集 看看他们提交的正确答案是什么 如果这样，请立即由助理回答。 具体查询内容不包含在帖子中 然后我得到了训练数据集。 这里还有一些更初步的…… 因为这个模型似乎能理解

### 1:19:53–1:20:15

EN：the statistically um the kinds of landmarks that are in this training set are usually the prominent landmarks the landmarks that people usually want to see the kinds of landmarks that are usually uh very often talked about on the internet and remember that the model already has a ton of Knowledge from its pre-training on the internet so it's probably seen a ton of conversations about Paris about landmarks about the kinds of things that

中文：统计学 嗯，这些地标的类型 这组训练集通常是 著名地标，即那些地标 人们通常想看到各种类型的 地标通常是……非常频繁 在互联网上讨论过， 请记住，该模型已经具有 从岗前培训中汲取的大量知识 在互联网上，它可能已经被浏览过。 关于巴黎的大量对话 关于这类事物的地标

### 1:20:15–1:20:37

EN：people like to see and so it's the pre-training knowledge that has then combined with the postering data set that results in this kind of an imitation um so that's uh that's roughly how you can kind of think about what's happening behind the scenes here in in this statistical sense okay now I want to turn to the topic of llm psychology as I like to call it which is what are sort

中文：人们喜欢看，所以它…… 培训前的知识，然后 结合海报数据集 这就导致了这种结果 模仿 所以，大概就是这样。 想想正在发生的事情。 这里幕后的情况是这样的 统计学知识不错，现在我想…… 我将转向心理学法学硕士这个话题。 我喜欢称它为“某种东西”。

## 11. hallucinations, tool use, knowledge/working memory（1:20:32–1:41:46）

### 1:20:37–1:21:02

EN：of the emergent cognitive effects of the training pipeline that we have for these models so in particular the first one I want to talk to is of course hallucinations so you might be familiar with model hallucinations it's when llms make stuff up they just totally fabricate information Etc and it's a big problem with llm assistants it is a problem that existed to a large extent with early models uh from many years ago

中文：新兴认知效应 我们针对这些项目制定的培训流程 模型，尤其是第一个模型，我 当然，我想和谁谈谈呢？ 幻觉，所以你可能很熟悉 伴随幻觉模型，当 llms 他们胡编乱造，简直 捏造信息等等，而且这很重要。 LLM 助手的问题在于…… 这个问题在很大程度上是存在的。 很多年前的早期型号

### 1:21:02–1:21:23

EN：and I think the problem has gotten a bit better uh because there are some medications that I'm going to go into in a second for now let's just try to understand where these hallucinations come from so here's a specific example of a few uh of three conversations that you might think you have in your training set and um these are pretty reasonable conversations that you could imagine being in the training set so

中文：我觉得这个问题有点…… 更好，因为有一些 我接下来要谈到的药物 稍等片刻，我们先试着…… 了解这些幻觉的来源 由此引申，以下是一个具体的例子。 在几次对话中，呃，大概三次吧。 你可能认为你拥有 训练集，嗯，这些相当 你可以进行一些合理的对话 想象一下自己身处训练组的样子

### 1:21:23–1:21:48

EN：like for example who is Cruz well Tom Cruz is an famous actor American actor and producer Etc who is John baraso this turns out to be a us senetor for example who is genis Khan well genis Khan was blah blah blah and so this is what your conversations could look like at training time now the problem with this is that when the human is writing the correct answer for the assistant in each

中文：例如，克鲁兹是谁？汤姆 克鲁兹是一位著名的美国演员。 还有制作人等等，他是约翰·巴拉索。 例如，结果发现他是一位美国参议员。 吉尼斯·汗是谁？嗯，吉尼斯·汗曾经是 巴拉巴拉巴拉，所以这就是你的 对话可能看起来像这样 现在的问题是，训练时间到了。 就是当人类写作的时候 每个助手给出的正确答案

### 1:21:48–1:22:07

EN：one of these cases uh the human either like knows who this person is or they research them on the Internet and they come in and they write this response that kind of has this like confident tone of an answer and what happens basically is that at test time when you ask for someone who is this is a totally random name that I totally came up with and I don't think this person exists um

中文：这些案例中，人类要么 比如知道这个人是谁，或者他们 在网上搜索他们，他们 他们进来后写下了这份回复。 那种感觉就像是自信满满。 回答的语气以及接下来发生的事情 基本上就是在考试的时候，当你 找个完全了解情况的人 我随手想出来的一个名字 我不认为这个人存在。

### 1:22:07–1:22:30

EN：as far as I know I just Tred to generate it randomly the problem is when we ask who is Orson kovats the problem is that the assistant will not just tell you oh I don't know even if the assistant and the language model itself might know inside its features inside its activations inside of its brain sort of it might know that this person is like not someone that um that is that it's

中文：据我所知，我只是用Tred生成 随机出现的问题就是当我们问的时候 奥森·科瓦茨是谁？问题是…… 助理不会只是告诉你哦 我甚至不知道助理是否 语言模型本身可能知道 在其特征内部 大脑内部的某种激活 它可能知道这个人像 不是那种人，嗯，就是那种人。

### 1:22:30–1:22:53

EN：familiar with even if some part of the network kind of knows that in some sense the uh saying that oh I don't know who this is is is not going to happen because the model statistically imitates is training set in the training set the questions of the form who is blah are confidently answered with the correct answer and so it's going to take on the style of the answer and it's going to do

中文：即使只熟悉其中一部分 网络在某种程度上知道这一点 呃，他说，哦，我不知道是谁 这不会发生。 因为该模型在统计学上模仿了 训练集在训练集中 问题形式为“谁是……” 自信地给出了正确的答案 答案是，它将承担起这个责任。 答案的风格，而且它会奏效。

### 1:22:53–1:23:13

EN：its best it's going to give you statistically the most likely guess and it's just going to basically make stuff up because these models again we just talked about it is they don't have access to the internet they're not doing research these are statistical token tumblers as I call them uh is just trying to sample the next token in the sequence and it's going to basically make stuff up so let's take a look at

中文：这是它能给你的最好结果 统计上最可能的猜测和 它基本上就是制造一些东西。 因为这些模型我们又一次…… 他们谈到这件事时说他们没有 他们无法访问互联网 这些研究是统计符号 我管它们叫“水杯”，呃，就是 尝试对下一个标记进行采样。 顺序，基本上 编造一些东西，让我们来看看。

### 1:23:13–1:23:37

EN：what this looks like I have here what's called the inference playground from hugging face and I am on purpose picking on a model called Falcon 7B which is an old model this is a few years ago now so it's an older model So It suffers from hallucinations and as I mentioned this has improved over time recently but let's say who is Orson kovats let's ask Falcon 7B instruct

中文：这看起来 就像我这里提到的…… 从拥抱脸部推断游乐场 我故意挑剔某个模特。 它被称为猎鹰7B，这是一个老型号 这已经是几年前的事了，所以…… 老款机型，所以它存在以下问题： 幻觉，正如我之前提到的那样 近年来情况有所改善，但 比如说，奥森·科瓦茨是谁？我们来问问。 猎鹰7B指令

### 1:23:37–1:24:04

EN：run oh yeah Orson kovat is an American author and science uh fiction writer okay this is totally false it's hallucination let's try again these are statistical systems right so we can resample this time Orson kovat is a fictional character from this 1950s TV show it's total BS right let's try again he's a former minor league baseball player okay so basically the model doesn't know and it's given us lots of

中文：跑吧，哦耶，奥森·科瓦特是美国人 作家兼科幻小说作家 好吧，这完全是假的。 幻觉，我们再试一次，这些是 统计系统没错，所以我们可以 这次重新采样 Orson kovat 是 这是20世纪50年代一部电视剧中的虚构人物。 证明这完全是胡说八道，对吧？我们再试一次。 他曾是一名小联盟棒球运动员。 玩家好的，所以基本上是模型 不知道，但这给了我们很多

### 1:24:04–1:24:29

EN：different answers because it doesn't know it's just kind of like sampling from these probabilities the model starts with the tokens who is oron kovats assistant and then it comes in here and it's get it's getting these probabilities and it's just sampling from the probabilities and it just like comes up with stuff and the stuff is actually statistically consistent with the style of the answer in its training set and

中文：答案各不相同，因为它并非如此。 我知道这有点像抽样。 根据这些概率，模型 以代币开始，其中谁是奥伦 科瓦茨的助手，然后它就进来了。 这里，它正在得到这些 概率，这只是抽样而已。 从概率上看，就像 想出一些东西，而这些东西是 实际上 在统计学上与该风格一致 答案在其训练集中

### 1:24:29–1:24:50

EN：it's just doing that but you and I experiened it as a madeup factual knowledge but keep in mind that uh the model basically doesn't know and it's just imitating the format of the answer and it's not going to go off and look it up uh because it's just imitating again the answer so how can we uh mitigate this because for example when we go to chat apt and I say who is oron kovats

中文：它就是这样，但你和我 感觉像是编造出来的事实 知识，但请记住，呃…… 模型基本上不知道，而且它是 只是模仿答案的格式。 它不会跑出去查看。 向上，因为它又在模仿了。 那么，我们该如何减轻这种影响呢？ 这是因为例如当我们去 聊天软件上，我问奥伦·科瓦茨是谁。

### 1:24:50–1:25:15

EN：and I'm now asking the stateoftheart state-of-the-art model from open AI this model will tell you oh so this model is actually is even smarter because you saw very briefly it said searching the web uh we're going to cover this later um it's actually trying to do tool use and uh kind of just like came up with some kind of a story but I want to just who

中文：我现在正在询问最新情况 来自 OpenAI 的最先进的模型 这个模型会告诉你 哦，所以这个模型实际上是…… 因为你只是匆匆一瞥，所以你更聪明了。 他说，在网上搜索一下，嗯，我们要…… 稍后再谈，嗯，它实际上是在尝试 使用工具和 呃，就想出了一些办法 这算是一个故事，但我只想知道是谁。

### 1:25:15–1:25:39

EN：or Kovach did not use any tools I don't want it to do web search there's a wellknown historical or public figure named or oron kovats so this model is not going to make up stuff this model knows that it doesn't know and it tells you that it doesn't appear to be a person that this model knows so somehow we sort of improved hallucinations even though they clearly

中文：或者说，科瓦奇没有使用任何我没有使用的工具。 想让它做网页 搜索一下，那里有一个著名的历史或 公众人物名为 oron kovats so 这个模型不会捏造事实。 这个模型知道它不知道 它会告诉你它没有出现。 成为这个模型所认识的人 不知怎么的，我们有所进步。 即使他们明显出现幻觉

### 1:25:39–1:26:02

EN：are an issue in older models and it makes totally uh sense why you would be getting these kinds of answers if this is what your training set looks like so how do we fix this okay well clearly we need some examples in our data set that where the correct answer for the assistant is that the model doesn't know about some particular fact but we only need to have those answers be produced

中文：老款车型存在这个问题，而且 完全可以理解你为什么会这样 如果能得到这类答案，那就太好了。 这就是你的训练集的样子。 我们该如何解决这个问题？好吧，显然我们 我们需要一些来自我们数据集的例子。 正确答案在哪里？ 助手表示该模型不知道 关于某个具体事实，但我们只 需要得出这些答案。

### 1:26:02–1:26:22

EN：in the cases where the model actually doesn't know and so the question is how do we know what the model knows or doesn't know well we can empirically probe the model to figure that out so let's take a look at for example how meta uh dealt with hallucinations for the Llama 3 series of models as an example so in this paper that they published from meta we can go into

中文：在模型实际 他不知道，所以问题是如何 我们是否了解模型所掌握的信息？ 不太清楚，我们可以通过经验来判断。 通过探测模型来找出答案 我们来看一个例子： 元呃处理幻觉 Llama 3 系列车型作为 例如，在本文中，他们 从元数据中发布，我们可以进入

### 1:26:22–1:26:50

EN：hallucinations which they call here factuality and they describe the procedure by which they basically interrogate the model to figure out what it knows and doesn't know to figure out sort of like the boundary of its knowledge and then they add examples to the training set where for the things where the model doesn't know them the correct answer is that the model doesn't know them which sounds like a very easy thing to do in

中文：幻觉 他们在这里称之为事实性，而且他们 描述他们采取的步骤 基本上就是对模型进行查询 弄清楚它知道什么，不知道什么。 知道如何弄清楚有点像 知识的边界，然后他们 将示例添加到训练集中， 对于模型无法处理的情况 知道他们的正确答案是 模型不知道它们，这听起来…… 就像一件非常容易做的事情一样

### 1:26:50–1:27:14

EN：principle but this roughly fixes the issue and the the reason it fixes the issue is because remember like the model might actually have a pretty good model of its self knowledge inside the network so remember we looked at the network and all these neurons inside the network you might imagine that there's a neuron somewhere in the network that sort of like lights up for when the model is

中文：原则上是这样，但这大致解决了这个问题。 问题及其解决方法 问题是 因为记住，就像模型可能那样 实际上，它有一个相当不错的模型。 因此，对网络内部的自我认知 还记得我们查看网络时吗？ 网络内部的所有这些神经元 可能会想象那里有一个神经元 网络的某个地方存在这种东西 就像模型亮起时一样

### 1:27:14–1:27:35

EN：uncertain but the problem is that the activation of that neuron is not currently wired up to the model actually saying in words that it doesn't know so even though the internal of the neural network no because there's some neurons that represent that the model uh will not surface that it will instead take its best guess so that it sounds confident um just like it sees in a

中文：虽然不确定，但问题在于…… 该神经元的激活并非 目前已连接到该模型 用言语表达它不知道。 即使神经内部 网络不，因为有一些神经元 这表示该模型将 不会出现这种情况，而是会采取 它的最佳猜测听起来如此 自信，就像它在……中看到的那样

### 1:27:35–1:27:55

EN：training set so we need to basically interrogate the model and allow it to say I don't know in the cases that it doesn't know so let me take you through what meta roughly does so basically what they do is here I have an example uh Dominic kek is uh the featured article today so I just went there randomly and what they do is basically they take a

中文：训练集，所以我们基本上需要 对模型进行查询并允许其 我说我不知道​​，在这种情况下 不知道，所以让我带你了解一下。 元到底做了什么？基本上是什么？ 他们在这里举个例子，嗯。 Dominic kek 是这篇专题文章的作者。 今天我只是随便去了那里。 他们所做的基本上就是……

### 1:27:55–1:28:23

EN：random document in a training set and they take a paragraph and then they use an llm to construct questions about that paragraph so for example I did that with chat GPT here so I said here's a paragraph from this document generate three specific factual questions based on this paragraph and give me the questions and the answers and so the llms are already good enough to create and reframe this

中文：训练集中的随机文档 他们选取一段文字，然后他们使用 一个法学硕士（LLM）来构建关于这方面的问题 例如，我用一段文字做了这件事。 聊天 GPT 所以我说，这是一段来自……的文字 本文档生成三个特定文件 基于此的事实性问题 段落，并给我提出问题。 答案以及 llms 已经存在 足以创造和重新构建这个

### 1:28:23–1:28:46

EN：information so if the information is in the context window um of this llm this actually works pretty well it doesn't have to rely on its memory it's right there in the context window and so it can basically reframe that information with fairly high accuracy so for example can generate questions for us like for which team did he play here's the answer how many cups did he win Etc and now

中文：信息，所以如果信息在 这个 llm 的上下文窗口 实际上效果还不错，但它并非如此。 必须依靠它的记忆，没错。 在上下文窗口中，就是这样。 基本上可以重新构建这些信息 例如，准确度相当高。 可以为我们生成类似这样的问题 他效力于哪支球队？答案如下。 他赢了多少座奖杯等等，现在

### 1:28:47–1:29:09

EN：what we have to do is we have some question and answers and now we want to interrogate the model so roughly speaking what we'll do is we'll take our questions and we'll go to our model which would be uh say llama uh in meta but let's just interrogate mol 7B here as an example that's another model so does this model know about this answer let's take a

中文：我们必须做的是，我们有一些 问答环节，现在我们想…… 粗略地质疑该模型 说到我们要做的事，我们会采取我们的 如有疑问，我们将介绍我们的模型。 那大概就是呃，说羊驼呃，在元认知里。 但我们先来这里查询一下 mol 7B。 例如，这是另一个模型。 这个模型知道这个答案吗？ 让我们来看一个

### 1:29:09–1:29:30

EN：look uh so he played for Buffalo Sabers right so the model knows and the the way that you can programmatically decide is basically we're going to take this answer from the model and we're going to compare it to the correct answer and again the model model are good enough to do this automatically so there's no humans involved here we can take uh basically the answer from the model and

中文：嗯，他曾效力于布法罗军刀队。 对，所以模型知道，而且方式 你可以通过编程方式决定是 基本上我们要采取这个 根据模型给出答案，我们将…… 将其与正确答案进行比较 再次强调，这些模型足够好。 自动执行此操作，因此不会出现任何问题。 这里涉及的人类，我们可以采取…… 基本上，模型给出的答案是……

### 1:29:30–1:29:55

EN：we can use another llm judge to check if that is correct according to this answer and if it is correct that means that the model probably knows so what we're going to do is we're going to do this maybe a few times so okay it knows it's Buffalo Savers let's drag in um Buffalo Sabers let's try one more time Buffalo Sabers so we asked three times about this factual question and

中文：我们可以使用另一位LLM法官来检查是否 根据这个答案，这是正确的。 如果这是正确的，那就意味着 模型可能知道，所以我们要去哪儿 我们要做的是，也许会这样做 几次之后，它就知道这是布法罗了。 省钱达人，让我们拖拽 嗯，布法罗军刀队，我们再试一次吧。 时间到了，所以我们问了三个关于布法罗军刀队的问题。 关于这个事实性问题的次数和

### 1:29:55–1:30:34

EN：the model seems to know so everything is great now let's try the second question how many Stanley Cups did he win and again let's interrogate the model about that and the correct answer is two so um here the model claims that he won um four times which is not correct right it doesn't match two so the model doesn't know it's making stuff up let's try again um so here the model again it's kind of like making stuff up right let's

中文：模型似乎知道一切，所以一切都…… 很好，现在我们来尝试第二个问题。 他一共赢得了多少座斯坦利杯？ 赢了，我们再来质问一下 关于该模型和正确答案 是 两个所以嗯，这里的模型声称他 赢了四次，这是不正确的。 对，它不匹配两个，所以模型 它不知道自己在编故事，我们来吧。 再试一次 嗯，这是模型，它有点像…… 就像编故事一样，对吧？

### 1:30:37–1:30:56

EN：Dragon here it says did he did not even did not win during his career so obviously the model doesn't know and the way we can programmatically tell again is we interrogate the model three times and we compare its answers maybe three times five times whatever it is to the correct answer and if the model doesn't know then we know that the model doesn't know this question and then what we do is we take this

中文：龙在这里说他甚至没有 职业生涯中从未赢得过冠军 显然，模型并不知道这一点。 我们可以通过编程方式再次告知 我们对模型进行三次查询 我们比较一下它的答案，也许三个 乘以五，再乘以这个值， 正确答案，如果模型不…… 那么我们就知道该模型不成立。 知道这个问题 然后我们所做的就是拿走这个

### 1:30:56–1:31:18

EN：question we create a new conversation in the training set so we're going to add a new conversation training set and when the question is how many Stanley Cups did he win the answer is I'm sorry I don't know or I don't remember and that's the correct answer for this question because we interrogated the model and we saw that that's the case if you do this for many different types of

中文：这个问题让我们开启了一场新的对话。 训练集，所以我们要添加一个 新的对话训练集以及何时 问题是，他们赢得了多少座斯坦利杯？ 他赢了吗？答案是，对不起，我 不知道或者我不记得了。 这是这个问题的正确答案。 因为我们质问了这个问题 模型显示情况确实如此。 你对许多不同类型的人都这样做

### 1:31:18–1:31:43

EN：uh questions for many different types of documents you are giving the model an opportunity to in its training set refuse to say based on its knowledge and if you just have a few examples of that in your training set the model will know um and and has the opportunity to learn the association of this knowledge-based refusal to this internal neuron somewhere in its Network that we presume

中文：呃，很多不同类型的问题 你提供给模型的文档 有机会参与其训练集 根据其所知，拒绝发表意见 如果你能举几个例子就好了。 模型将知道，在你的训练集中，它将会知道 嗯，并且有机会学习 这种基于知识的关联 拒绝这种内部神经元 在其网络的某个地方，我们推测

### 1:31:43–1:32:08

EN：exists and empirically this turns out to be probably the case and it can learn that Association that hey when this neuron of uncertainty is high then I actually don't know and I'm allowed to say that I'm sorry but I don't think I remember this Etc and if you have these uh examples in your training set then this is a large mitigation for hallucination and that's roughly speaking why chpt is able to do stuff

中文：存在，并且经验表明这一点 很可能如此，而且它还能学习 那个协会，嘿，当这 那么，当神经元的不确定性水平很高时，我 其实我不知道，而且我有权知道。 说声对不起，但我并不认为 记住这一点等等，如果你有这些 呃，训练集中的例子 这是一项重要的缓解措施 幻觉，大概就是这样。 解释一下为什么 chpt 能做到这些

### 1:32:08–1:32:33

EN：like this as well so these are kinds of uh mitigations that people have implemented and that have improved the factuality issue over time okay so I've described mitigation number one for basically mitigating the hallucinations issue now we can actually do much better than that uh it's instead of just saying that we don't know uh we can introduce an additional mitigation number two to give the llm an opportunity to be

中文：像这样的也一样，所以这些都是某种类型的 呃，人们采取的缓解措施 已实施并改进了 随着时间的推移，事实问题出现了，好吧，所以我…… 针对缓解措施一，已描述如下 基本上就是减轻幻觉 现在的问题是，我们其实可以做得更好。 比那更确切地说，与其只是说…… 我们不知道，呃，我们可以介绍 第二项额外缓解措施 给法学硕士一个机会

### 1:32:33–1:32:54

EN：factual and actually answer the question now what do you and I do if I was to ask you a factual question and you don't know uh what would you do um in order to answer the question well you could uh go off and do some search and uh use the internet and you could figure out the answer and then tell me what that answer is and we can do the exact exact same

中文：符合事实，并真正回答问题 如果我问你，你我该怎么办？ 你提出了一个事实性问题，而你没有 你知道你会怎么做吗？ 回答这个问题，你可以…… 关掉，搜索一下，然后……使用 上网你就能找到答案了。 请回答，然后告诉我这个答案是什么。 是的，我们也可以做完全相同的事情。

### 1:32:54–1:33:17

EN：thing with these models so think of the knowledge inside the neural network inside its billions of parameters think of that as kind of a vague recollection of the things that the model has seen during its training during the pre-training stage a long time ago so think of that knowledge in the parameters as something you read a month ago and if you keep reading something then you will remember it and the model

中文：想想这些模型的一些问题…… 神经网络内部的知识 在其数十亿个参数之内思考 那件事给我留下了一种模糊的印象。 该模型所看到的事物 在训练期间 很久以前的预备训练阶段了，所以 想想这些知识 参数就像你每月读到的内容一样。 很久以前，如果你继续阅读某些内容 这样你就会记住它和这个模型。

### 1:33:17–1:33:34

EN：remembers that but if it's something rare then you probably don't have a really good recollection of that information but what you and I do is we just go and look it up now when you go and look it up what you're doing basically is like you're refreshing your working memory with information and then you're able to sort of like retrieve it talk about it or Etc so we need some

中文：记得，但如果是其他什么事的话 这种情况很少见，所以你可能没有 对那件事的记忆力真好。 信息，但你我所做的是…… 你现在去的时候就去查一下吧。 查查你在做什么 基本上就像你在刷新你的 工作记忆中的信息，然后 你可以把它找回来。 谈谈这件事等等，所以我们需要一些

### 1:33:34–1:33:57

EN：equivalent of allowing the model to refresh its memory or its recollection and we can do that by introducing tools uh for the models so the way we are going to approach this is that instead of just saying hey I'm sorry I don't know we can attempt to use tools so we can create uh a mechanism by which the language model can emit special tokens and these are tokens that

中文：相当于允许模型 唤起记忆或回忆 我们可以通过引入工具来实现这一点。 呃，为了 模型，所以我们将采用这种方式 这种方法就是，而不是仅仅 说“嘿，对不起，我不知道我们可以……” 尝试使用工具，以便我们能够创建…… 机制 语言模型可以通过这种方式发出 特殊代币，这些是……

### 1:33:57–1:34:20

EN：we're going to introduce new tokens so for example here I've introduced two tokens and I've introduced a format or a protocol for how the model is allowed to use these tokens so for example instead of answering the question when the model does not instead of just saying I don't know sorry the model has the option now to emitting the special token search start and this is the query that will go

中文：我们将推出新的代币，所以 例如，这里我介绍了两个 代币，我已经引入了一种格式或一种 模型如何被允许的协议 例如，请使用这些令牌代替 当模型回答这个问题时 不，而不是直接说我不 抱歉，该型号现在有此选项。 发出特殊令牌搜索 开始，以下是即将执行的查询。

### 1:34:20–1:34:44

EN：to like bing.com in the case of openai or say Google search or something like that so it will emit the query and then it will emit search end and then here what will happen is that the program that is sampling from the model that is running the inference when it sees the special token search end instead of sampling the next token uh in the sequence it will actually pause

中文：就像 openai 中的 bing.com 一样 或者说谷歌搜索之类的。 这样它就会发出查询，然后 它将发出搜索结束信号，然后在这里 接下来会发生的情况是，该程序 这是从模型中抽样。 当检测到以下内容时，运行推理： 特殊标记搜索结束，而不是 对下一个标记进行采样 这段序列实际上会暂停

### 1:34:44–1:35:05

EN：generating from the model it will go off it will open a session with bing.com and it will paste the search query into Bing and it will then um get all the text that is retrieved and it will basically take that text it will maybe represent it again with some other special tokens or something like that and it will take that text and it will copy paste it here

中文：根据模型生成的数据，它将停止运行。 它将打开与 bing.com 的会话， 它会将搜索查询粘贴到必应中。 然后它会获取所有文本 已检索到，并且基本上 这段文字或许代表 它又加上了一些其他特殊标记 或者类似的事情，这需要…… 这段文字会被复制粘贴到这里。

### 1:35:05–1:35:25

EN：into what I Tred to like show with the brackets so all that text kind of comes here and when the text comes here it enters the context window so the model so that text from the web search is now inside the context window that will feed into the neural network and you should think of the context window as kind of like the working memory of the model

中文：进入我喜欢的节目 所以所有这些文字都用括号括起来了。 这里，当文本出现在这里时 进入上下文窗口，因此模型 因此，来自网络搜索的文本现在是 在上下文窗口中，它将提供 进入神经网络，你应该 把上下文窗口想象成某种…… 就像模型的工作记忆一样

### 1:35:25–1:35:48

EN：that data that is in the context window is directly accessible by the model it directly feeds into the neural network so it's not anymore a vague recollection it's data that it it has in the context window and is directly available to that model so now when it's sampling the new uh tokens here afterwards it can reference very easily the data that has been copy pasted in there so that's

中文：上下文窗口中的数据 可由模型直接访问 直接输入神经网络 所以这不再是模糊的记忆了。 这是它在上下文中拥有的数据。 窗口可直接访问。 所以现在当它对新模型进行采样时 呃，这里的代币之后可以 可以非常方便地引用这些数据。 是复制粘贴进去的，所以就是这样。

### 1:35:48–1:36:08

EN：roughly how these um how these tools use uh tools uh function and so web search is just one of the tools we're going to look at some of the other tools in a bit uh but basically you introduce new tokens you introduce some schema by which the model can utilize these tokens and can call these special functions like web search functions and how do you teach the model

中文：这些工具大概是如何使用的 呃 工具 呃 功能 因此，网络搜索只是其中之一。 我们将要了解的一些工具 还有一些其他工具，嗯，但基本上 您引入新的代币，您引入 模型可以通过某种模式进行建模。 利用这些令牌，可以调用这些令牌。 特殊功能，例如网络搜索 函数以及如何教授该模型

### 1:36:08–1:36:30

EN：how to correctly use these tools like say web search search start search end Etc well again you do that through training sets so we need now to have a bunch of data and a bunch of conversations that show the model by example how to use web search so what are the what are the settings where you are using the search um and what does that look like and here's by example how

中文：如何正确使用这些工具，例如 假设网络搜索开始搜索结束 等等，你又通过这种方式做到了。 所以我们现在需要一些训练集。 一堆数据和一堆 通过对话展现该模型 例如如何使用网络搜索，那么…… 有哪些设置？ 正在使用搜索功能，嗯，那又怎样？ 看起来像这样，下面我举个例子来说明。

### 1:36:30–1:36:49

EN：you start a search and the search Etc and uh if you have a few thousand maybe examples of that in your training set the model will actually do a pretty good job of understanding uh how this tool works and it will know how to sort of structure its queries and of course because of the pre-training data set and its understanding of the world it actually kind of understands what a web

中文：你开始搜索，然后搜索结果等等 呃，如果你有几千块钱的话，也许 训练集中的例子 该模型实际上会表现得相当不错。 理解这个工具的工作 它能工作，而且它知道如何…… 构建查询结构，当然还有 由于预训练数据集和 它对世界的理解 实际上他有点理解什么是网络

### 1:36:49–1:37:08

EN：search is and so it actually kind of has a pretty good native understanding um of what kind of stuff is a good search query um and so it all kind of just like works you just need a little bit of a few examples to show it how to use this new tool and then it can lean on it to retrieve information and uh put it in the context window and that's

中文：搜索就是，所以它实际上有点…… 对母语人士的理解相当不错 嗯，什么样的东西才算好东西？ 搜索查询嗯，所以这一切都有点…… 就像工作一样，你只需要一点点 举几个例子来说明如何操作 使用这个新工具，它就可以学习了。 在上面检索信息，然后…… 它出现在上下文窗口中，就是这样。

### 1:37:08–1:37:29

EN：equivalent to you and I looking something up because once it's in the context it's in the working memory and it's very easy to manipulate and access so that's what we saw a few minutes ago when I was searching on chat GPT for who is Orson kovats the chat GPT language model decided Ed that this is some kind of a rare um individual or something like that and instead of giving me an

中文：相当于你我看着 出了点问题，因为一旦它进入了 上下文：它存在于工作记忆中。 它非常容易操控和访问。 这就是我们几分钟前看到的。 当我在聊天 GPT 中搜索“谁”时 Orson kovats 是聊天 GPT 语言吗 模型决定艾德这是某种 罕见的个体之类的 就这样，而不是给我一个

### 1:37:29–1:37:50

EN：answer from its memory it decided that it will sample a special token that is going to do web search and we saw briefly something flash it was like using the web tool or something like that so it briefly said that and then we waited for like two seconds and then it generated this and you see how it's creating references here and so it's citing sources so what happened here is

中文：它从记忆中找到了答案，并决定 它将对一个特殊的标记进行采样，该标记是 准备上网搜索，我们看到 就像一道闪光，短暂地闪过。 使用网络工具或类似工具 所以它简要地说明了这一点，然后我们 等了大概两秒钟，然后它 生成了这个，你看它是怎么生成的 这里创建了参考文献，所以就是这样。 引用消息来源，这里发生的事情是：

### 1:37:50–1:38:15

EN：it went off it did a web web search it found these sources and these URLs and the text of these web pages was all stuffed in between here and it's not showing here but it's it's basically stuffed as text in between here and now it sees that text and now it kind of references it and says that okay it could be these people citation could be those people citation Etc so that's what

中文：它启动了，它进行了网络搜索。 找到了这些资源和这些网址， 这些网页上的文字都是 它被夹在中间，但它不是。 这里显示的是，但基本上是 塞满文字，介于此时此地之间 它看到了那段文字，现在它有点…… 引用它并说好的 这些人可能是引文 那些人引用等等，就是这样。

### 1:38:15–1:38:39

EN：happened here and that's what and that's why when I said who is Orson kovats I could also say don't use any tools and then that's enough to um basically convince chat PT to not use tools and just use its memory and its recollection I also went off and I um tried to ask this question of Chachi PT so how many standing cups did uh Dominic Hasek win and Chachi P actually decided

中文：这里发生了这件事，就是这样。 为什么当我问奥森·科瓦茨是谁时 也可以说不要使用任何工具， 那么这就足够了…… 基本上就是说服聊天PT不要使用 工具，只需使用其内存和它的 我记得我也离开了，嗯…… 我试着问Chachi PT这个问题。 那么，多米尼克一共喝了多少杯立杯？ 哈谢克获胜，查奇·P实际上决定了胜负。

### 1:38:39–1:39:05

EN：that it knows the answer and it has the confidence to say that uh he want twice and so it kind of just relied on its memory because presumably it has um it has enough of a kind of confidence in its weights in it parameters and activations that this is uh retrievable just for memory um but you can also conversely use web search to make sure and then for the same query it actually

中文：它知道答案，而且它拥有 他有信心说他想要两次 所以它基本上只能依靠它自身。 内存，因为它大概有……嗯…… 已经足够了 对自身权重的一种自信 它参数和激活方式 呃，只是为了内存可以检索，嗯，但是 你也可以 反之，也可以使用网络搜索来确认。 然后对于同一个查询，它实际上

### 1:39:06–1:39:29

EN：goes off and it searches and then it finds a bunch of sources it finds all this all of this stuff gets copy pasted in there and then it tells us uh to again and sites and it actually says the Wikipedia article which is the source of this information for us as well so that's tools web search the model determines when to search and then uh that's kind of like how these tools uh

中文：它启动并搜索，然后它 它找到了很多来源，它找到了所有 所有这些东西都是复制粘贴的。 里面，然后它告诉我们呃 再次，网站也确实如此说。 维基百科文章，即来源 这些信息对我们来说也很有用。 那是工具，网络搜索模型 决定何时进行搜索，然后呃 这有点像这些工具的运作方式……

### 1:39:29–1:39:55

EN：work and this is an additional kind of mitigation for uh hallucinations and factuality so I want to stress one more time this very important sort of psychology Point knowledge in the parameters of the neural network is a vague recollection the knowledge in the tokens that make up the context window is the working memory and it roughly speaking Works kind of like um it works for us in our brain the stuff

中文：工作，这是另一种类型的 缓解幻觉和 事实就是如此，所以我还要强调一点。 这段时间非常重要 心理学 参数中的点知识 神经网络是一种模糊的记忆 构成代币的知识 上下文 窗口就是工作内存，而且 粗略地说，运作方式有点像…… 它对我们的大脑起作用。

### 1:39:55–1:40:17

EN：we remember is our parameters uh and the stuff that we just experienced like a few seconds or minutes ago and so on you can imagine that being in our context window and this context window is being built up as you have a conscious experience around you so this has a bunch of um implications also for your use of LOLs in practice so for example I can go to chat GPT and I can do

中文：我们记住的是我们的参数，呃，还有 我们刚刚经历的事情就像…… 几秒钟或几分钟前，等等。 可以想象，在我们这种语境下，情况会是怎样的。 窗口，并且此上下文窗口正在被 随着你意识的增强而逐渐形成 你周围的经验，所以这很有价值。 这其中也包含着很多嗯……对你的影响 LOL 的实际应用，例如我 可以去聊天 GPT，我可以做

### 1:40:17–1:40:37

EN：something like this I can say can you Summarize chapter one of Jane Austin's Pride and Prejudice right and this is a perfectly fine prompt and Chach actually does something relatively reasonable here and but the reason it does that is because Chach has a pretty good recollection of a famous work like Pride and Prejudice it's probably seen a ton of stuff about it there's probably forums about this book it's probably

中文：类似这样的话，我可以这么说吗？ 概括简·奥斯汀作品的第一章 《傲慢与偏见》没错，这就是 完全没问题，而且Chach实际上 做一些相对合理的事情 这里，但它这样做的原因是 因为查奇的成绩相当不错 回忆起像《傲慢与偏见》这样的著名作品 《偏见与偏见》这部电影可能已经被看过很多遍了。 关于它，可能有很多东西。 关于这本书的论坛可能

### 1:40:37–1:40:59

EN：read versions of this book um and it's kind of like remembers because even if you've read this or articles about it you'd kind of have a recollection enough to actually say all this but usually when I actually interact with LMS and I want them to recall specific things it always works better if you just give it to them so I think a much better prompt would be something like this can you

中文：读过这本书的不同版本，嗯，它是 有点像记得，因为即使 你读过这篇文章或相关文章吗？ 你大概会有一些记忆吧。 实际上要说这些，但通常 当我实际与LMS交互时，我 希望他们回忆起特定的事情 如果你直接给它，效果总是更好。 所以我觉得这是一个很好的提示 大概是这样的，可以吗？

### 1:40:59–1:41:20

EN：summarize for me chapter one of genos's spr and Prejudice and then I am attaching it below for your reference and then I do something like a delimeter here and I paste it in and I I found that just copy pasting it from some website that I found here um so copy pasting the chapter one here and I do that because when it's in the context window the model has direct access to it

中文：请帮我概括一下杰诺斯的第一章 spr 和偏见，然后我 附件如下，供您参考。 然后我做了类似分界线之类的事情 我把它粘贴到这里，然后我找到了 就是从某个地方复制粘贴过来的。 我在这里找到的网站，嗯，所以复制 我把第一章的内容粘贴到这里，我 因为当它在那种语境下…… 模型可以直接访问窗口

### 1:41:20–1:41:40

EN：and can exactly it doesn't have to recall it it just has access to it and so this summary is can be expected to be a significantly high quality or higher quality than this summary uh just because it's directly available to the model and I think you and I would work in the same way if you want to it would be you would produce a much better summary if you had reread this chapter

中文：而且完全可以，不一定非得如此 请记住，它只是有访问权限而已。 因此，可以预期这份摘要将是： 质量显著高或更高 比这篇总结的质量高得多，呃，就 因为它可以直接供……使用 模特，我觉得你我都能胜任。 同样地，如果你愿意的话，它也可以。 你会做出更好的作品。 如果你重读了这一章，以下是概要。

### 1:41:40–1:42:01

EN：before you had to summarize it and that's basically what's happening here or the equivalent of it the next sort of psychological Quirk I'd like to talk about briefly is that of the knowledge of self so what I see very often on the internet is that people do something like this they ask llms something like what model are you and who built you and um basically this uh question is a

中文：之前你必须总结一下 基本上，这里发生的事情就是这样。 或者等价于它的下一类 我想谈谈我的心理怪癖。 简而言之，就是知识。 自我，所以我经常在……上看到 互联网就是人们做某事的地方。 他们会这样问LLMS类似这样的问题 你是什​​么型号的？谁制造的？ 嗯，基本上这个问题是……

## 12. knowledge of self（1:41:46–1:46:56）

### 1:42:01–1:42:21

EN：little bit nonsensical and the reason I say that is that as I try to kind of explain with some of the underhood fundamentals this thing is not a person right it doesn't have a persistent existence in any way it sort of boots up processes tokens and shuts off and it does that for every single person it just kind of builds up a context window of conversation and then everything gets

中文：有点莫名其妙，原因如下 也就是说，当我试图……的时候 用一些底层原理来解释一下 从根本上讲，这东西不是人 对，它没有持久性。 无论以何种方式存在，它都会启动。 处理令牌并关闭，然后它 它对每个人都这样做。 这只是构建一个上下文窗口而已。 对话开始后，一切都变得……

### 1:42:21–1:42:42

EN：deleted and so this this entity is kind of like restarted from scratch every single conversation if that makes sense it has no persistent self it has no sense of self it's a token tumbler and uh it follows the statistical regularities of its training set so it doesn't really make sense to ask it who are you what build you Etc and by default if you do what I described and

中文：已删除，因此这个实体是某种 就像一切都从头开始一样 如果这能说得通的话，那就是一次简单的对话。 它没有持久的自我，它没有 自我意识就像一个象征性的翻滚器。 嗯，它遵循统计学原理。 它的训练集具有规律性，因此 问它“是谁”其实没什么意义。 你是什​​么造就了你等等，以及通过 如果你按照我描述的方式操作，默认是这样的

### 1:42:42–1:43:04

EN：just by default and from nowhere you're going to get some pretty random answers so for example let's uh pick on Falcon which is a fairly old model and let's see what it tells us uh so it's evading the question uh talented engineers and developers here it says I was built by open AI based on the gpt3 model it's totally making stuff up now the fact that it's built by open

中文：就凭空，你就是默认的。 将会得到一些非常随机的答案 举个例子，我们来拿猎鹰说事儿吧。 这是一个相当老旧的型号，我们来看看 看看它怎么说 我们呃，所以这是在回避问题呃 这里汇聚了众多才华横溢的工程师和开发人员。 它说我是由 OpenAI 基于……构建的 GPT-3模型完全是在制造东西 现在的问题是，它是由开源软件构建的。

### 1:43:04–1:43:29

EN：AI here I think a lot of people would take this as evidence that this model was somehow trained on open AI data or something like that I don't actually think that that's necessarily true the reason for that is that if you don't explicitly program the model to answer these kinds of questions then what you're going to get is its statistical best guess at the answer and this model had a um sft data mixture of

中文：我认为很多人都会喜欢人工智能。 将此视为该模型的证据 以某种方式使用 OpenAI 数据进行训练或 类似的事情，我其实并不了解。 认为这必然是正确的 原因在于 如果你不显式地对……进行编程 回答这类问题的模型 那么你将得到的就是它的 统计学上对答案的最佳猜测和 该模型具有 um sft 数据混合

### 1:43:29–1:43:55

EN：conversations and during the fine-tuning um the model sort of understands as it's training on this data that it's taking on this personality of this like helpful assistant and it doesn't know how to it doesn't actually it wasn't told exactly what label to apply to self it just kind of is taking on this uh this uh Persona of a helpful assistant and remember that the pre-training stage took the

中文：对话和期间 对模型进行微调之类的 明白这是在接受这方面的训练。 它正在收集这方面的数据 这种性格的人乐于助人。 助手，但它不知道该怎么做。 实际上并没有人明确告诉过我。 该给自己贴什么标签呢？就这么简单。 正在扮演这个呃这个呃人格面具 记住，有个乐于助人的助手很重要。 预备训练阶段

### 1:43:55–1:44:17

EN：documents from the entire internet and Chach and open AI are very prominent in these documents and so I think what's actually likely to be happening here is that this is just its hallucinated label for what it is this is its self-identity is that it's chat GPT by open Ai and it's only saying that because there's a ton of data on the internet of um answers like this that are actually

中文：来自整个互联网的文档和 Chach 和 OpenAI 在人工智能领域非常突出 这些文件，所以我认为是什么呢？ 这里真正可能发生的情况是 这只是它幻觉般的标签而已。 这就是它的自我认同。 它是由 OpenAI 开发的聊天 GPT， 它这么说只是因为存在一个 互联网上有海量的数据 像这样的答案实际上是

### 1:44:17–1:44:39

EN：coming from open from chasht and So that's its label for what it is now you can override this as a developer if you have a llm model you can actually override it and there are a few ways to do that so for example let me show you there's this MMO model from Allen Ai and um this is one llm it's not a top tier LM or anything like that but I like it

中文：来自 chasht 和 So 的开放 这就是它现在的标签。 作为开发者，您可以覆盖此设置。 拥有一个法学硕士（LLM）模型，你实际上可以 可以覆盖它，有几种方法可以做到这一点。 这样做，例如，让我来演示一下。 Allen Ai 有一个 MMO 模型， 嗯，这是其中之一，它不是顶级的。 LM之类的名字也行，反正我喜欢。

### 1:44:39–1:44:58

EN：because it is fully open source so the paper for Almo and everything else is completely fully open source which is nice um so here we are looking at its sft mixture so this is the data mixture of um the fine tuning so this is the conversations data it right and so the way that they are solving it for Theo model is we see that there's a bunch of

中文：因为它完全开源，所以 Almo 的纸张以及其他所有东西都是 完全开源 嗯，不错，我们现在看到的是它的 sft混合物，所以这是数据混合物 嗯，微调一下，所以这是…… 对话数据是正确的，所以 他们为西奥解决这个问题的方式 模型是，我们看到有很多

### 1:44:58–1:45:23

EN：stuff in the mixture and there's a total of 1 million conversations here but here we have alot to hardcoded if we go there we see that this is 240 conversations and look at these 240 conversations they're hardcoded tell me about yourself says user and then the assistant says I'm and open language model developed by AI to Allen Institute of artificial intelligence Etc I'm here to help blah blah blah what is your name

中文：混合物中含有各种物质，总共有…… 这里有一百万条对话，但在这里 如果我们去那里，就有很多东西需要硬编码。 我们看到这是240。 对话，看看这240个 对话是硬编码的，它们告诉我 用户说“关于你自己”，然后是 助理说我是开放语言 人工智能为艾伦研究所开发的模型 人工智能等等，我在这里 帮忙等等等等，你叫什么名字？

### 1:45:23–1:45:46

EN：uh Theo project so these are all kinds of like cooked up hardcoded questions abouto 2 and the correct answers to give in these cases if you take 240 questions like this or conversations put them into your training set and fine tune with it then the model will actually be expected to parot this stuff later if you don't give it this then it's probably a Chach by open

中文：呃，Theo 项目，所以这些都是各种各样的 就像预先编造好的硬编码问题 关于 2 和正确答案 在这种情况下，如果你回答 240 道题 像这样，或者对话将它们带入 你的训练集，并用它进行微调 那么，该模型实际上就会被预期。 如果你不这样做，以后再模仿这些东西吧 如果给它这个，那它很可能就是个查奇 通过开放

### 1:45:46–1:46:10

EN：Ai and um there's one more way to sometimes do this is that basically um in these conversations and you have terms between human and assistant sometimes there's a special message called system message at the very beginning of the conversation so it's not just between human and assistant there's a system and in the system message you can actually hardcode and remind the model that hey you are a

中文：人工智能，还有另一种方法 有时这样做是 基本上，在这些对话中 人类之间存在着各种关系。 助理有时会有特殊情况 名为系统消息的消息 对话伊始 这不仅仅是人类之间的问题 助手那里有一个系统，而且在 系统消息实际上可以硬编码 并提醒模特，嘿，你是一个

### 1:46:10–1:46:30

EN：model developed by open Ai and your name is chashi pt40 and you were trained on this date and your knowledge cut off is this and basically it kind of like documents the model a little bit and then this is inserted into to your conversations so when you go on chpt you see a blank page but actually the system message is kind of like hidden in there and those tokens are in the context

中文：由 OpenAI 和您的名字开发的模型 是 chashi pt40，你接受过相关培训吗？ 这个日期和你的知识截止点是 这个，基本上有点像…… 对该模型进行了一些文档记录，并且 然后将其插入到您的 所以当你进入下一章时，对话就会开始。 看到一张空白页，但实际上系统 信息有点像隐藏在里面。 这些标记都位于上下文中。

### 1:46:30–1:46:51

EN：window and so those are the two ways to kind of um program the models to talk about themselves either it's done through uh data like this or it's done through system message and things like that basically invisible tokens that are in the context window and remind the model of its identity but it's all just kind of like cooked up and bolted on in some in some way it's not actually like

中文：窗口，所以这就是两种方法。 某种程度上，嗯，给模型编写程序，让它们能够对话。 关于他们自己，要么已经完成了。 通过这样的数据，或者说，就是这样。 通过系统消息等等 基本上是不可见的令牌 在上下文窗口中并提醒 它的身份模型，但这仅仅是 有点像是临时炒制然后硬塞上去的。 在某种程度上，它实际上并非如此

### 1:46:51–1:47:13

EN：really deeply there in any real sense as it would before a human I want to now continue to the next section which deals with the computational capabilities or like I should say the native computational capabilities of these models in problem solving scenarios and so in particular we have to be very careful with these models when we construct our examples of conversations and there's a lot of sharp edges here

中文：在任何真正的意义上，都深深地存在着 它比我想要的人类还要早 继续下一节，该节将讨论…… 具备计算能力或 就像我应该说的，本地人 这些的计算能力 问题解决场景中的模型和 所以，我们尤其要非常 当我们使用这些模型时要格外小心。 构建我们的对话示例 这里有很多尖锐的边缘。

## 13. models need tokens to think（1:46:56–2:01:11）

### 1:47:13–1:47:34

EN：that are kind of like elucidative is that a word uh they're kind of like interesting to look at when we consider how these models think so um consider the following prompt from a human and supposed that basically that we are building out a conversation to enter into our training set of conversations so we're going to train the model on this we're teaching you how to basically solve simple math problems so the prompt

中文：有点像阐释性的 那个词，呃，他们有点像 当我们考虑这个问题时，这很有意思。 这些模型是如何思考的，所以……考虑一下 以下提示来自人类和 假设我们基本上是 构建对话以进入 加入我们的对话训练集 所以我们将对模型进行训练 我们正在教你如何基本上 解决简单的数学题，以便提示

### 1:47:34–1:47:56

EN：is Emily buys three apples and two oranges each orange cost $2 the total cost is 13 what is the cost of apples very simple math question now there are two answers here on the left and on the right they are both correct answers they both say that the answer is three which is correct but one of these two is a significant ific anly better answer for the assistant than the other like if I

中文：艾米丽买了三个苹果和两个 每个橙子售价 2 美元，总共 苹果的价格是13，那么苹果的价格是多少？ 这是一个非常简单的数学题，现在有…… 这里有两个答案，左边一个，右边一个。 没错，它们都是正确答案。 两者都说答案是三，哪个 正确，但这两者中有一个是 显著的 ific 和更好的答案 助理比其他助理更像，如果我

### 1:47:56–1:48:17

EN：was Data labeler and I was creating one of these one of these would be uh a really terrible answer for the assistant and the other would be okay and so I'd like you to potentially pause the video Even and think through why one of these two is significantly better answer uh than the other and um if you use the wrong one your model will actually be uh

中文：当时我正在创建数据标签器。 这些其中之一就是呃…… 对助理来说，这真是个糟糕的回答。 另一个也可以，所以我会 比如你可以暂停视频。 甚至仔细思考一下为什么其中一个 二是明显更好的答案。 比其他方式，嗯，如果你使用 错了，你的模型实际上是……

### 1:48:17–1:48:37

EN：really bad at math potentially and it would have uh bad outcomes and this is something that you would be careful with in your life labeling documentations when you are training people uh to create the ideal responses for the assistant okay so the key to this question is to realize and remember that when the models are training and also inferencing they are working in onedimensional sequence of tokens from

中文：可能数学真的很差 会造成不好的后果，而这是 你需要小心谨慎的事情 在你的生活中标记文档 当你培训人们的时候 创建理想的应对方案 助理好的，所以关键在于…… 问题在于要意识到并记住这一点。 当模型正在训练时，以及 推断他们正在工作 来自一维标记序列

### 1:48:37–1:48:58

EN：left to right and this is the picture that I often have in my mind I imagine basically the token sequence evolving from left to right and to always produce the next token in a sequence we are feeding all these tokens into the neural network and this neural network then is the probabilities for the next token and sequence right so this picture here is the exact same picture we saw uh before

中文：从左到右，这就是这张照片。 我脑海中经常浮现的画面是这样的： 基本上，令牌序列在不断演变。 从左到右，并且始终产生 序列中的下一个标记是 将所有这些标记输入到神经网络中 网络，而这个神经网络则是 下一个令牌的概率和 顺序对，所以这张图片是 我们之前看到的那张照片一模一样。

### 1:48:58–1:49:22

EN：up here and this comes from the web demo that I showed you before right so this is the calculation that basically takes the input tokens here on the top and uh performs these operations of all these neurons and uh gives you the answer for the probabilities of what comes next now the important thing to realize is that roughly speaking uh there's basically a finite number of layers of computation that

中文：这里的内容来自网页演示。 我之前给你看过的，对吧？所以这个 基本上，计算过程需要 顶部的输入标记，呃…… 对所有这些执行这些操作 神经元，嗯，它会给你答案 接下来发生的事情的概率 需要认识到的重要一点是： 大致 呃，基本上是有限的 计算层数

### 1:49:22–1:49:46

EN：happened here so for example this model here has only one two three layers of what's called detention and uh MLP here um maybe um typical modern state-of-the-art Network would have more like say 100 layers or something like that but there's only 100 layers of computation or something like that to go from the previous token sequence to the probabilities for the next token and so there's a finite amount of computation

中文：这里就发生了这种情况，例如这个模型 这里只有一层、两层、三层。 这里所谓的拘留和MLP是什么？ 嗯，也许，嗯，典型的现代 最先进的网络将拥有更多 比如说100层之类的 但是只有100层 进行计算之类的操作 从前一个标记序列到 下一个令牌的概率等等 计算量是有限的。

### 1:49:46–1:50:09

EN：that happens here for every single token and you should think of this as a very small amount of computation and this amount of computation is almost roughly fixed uh for every single token in this sequence um the that's not actually fully true because the more tokens you feed in uh the the more expensive uh this forward pass will be of this neural network but not by much so you should

中文：这种情况发生在这里，每个代币都会发生这种情况。 你应该把这看作是一个非常 计算量很小，而且 计算量几乎大致为 固定了 uh，适用于此中的每个标记。 序列，嗯，那实际上并不是 完全正确，因为代币越多你 饲料价格更高 这个前向传播将是这个神经的 网络，但差距不大，所以你应该

### 1:50:09–1:50:25

EN：think of this uh and I think as a good model to have in mind this is a fixed amount of compute that's going to happen in this box for every single one of these tokens and this amount of compute Cann possibly be too big because there's not that many layers that are sort of going from the top to bottom here there's not that that much computationally that will happen here

中文：想想这个，嗯，我认为这很好 要记住的模型是固定的 即将发生的计算量 这个盒子里装着每一个 这些代币和这些计算量 Cann 可能太大了，因为有 没有那么多层，有点像 从上到下 其实没那么多。 从计算角度来看，这将在这里发生。

### 1:50:26–1:50:50

EN：and so you can't imagine the model to to basically do arbitrary computation in a single forward pass to get a single token and so what that means is that we actually have to distribute our reasoning and our computation across many tokens because every single token is only spending a finite amount of computation on it and so we kind of want to distribute the computation across many tokens and we can't have too much

中文：所以你无法想象这个模型 基本上可以进行任意计算 单次前传球获得一个 令牌，所以这意味着我们 实际上我们必须分发我们的 推理和我们的计算 许多代币，因为每个代币 只是花费有限的金额 对此进行计算，所以我们有点想要 将计算任务分配到 代币很多，我们永远不会嫌多。

### 1:50:50–1:51:16

EN：computation or expect too much computation out of of the model in any single individual token because there's only so much computation that happens per token okay roughly fixed amount of computation here so that's why this answer here is significantly worse and the reason for that is Imagine going from left to right here um and I copy pasted it right here the answer is three Etc imagine the

中文：计算或期望过高 任何模型的计算结果 因为只有一个单独的代币。 仅发生一定量的计算。 每个代币的金额大致固定。 此处计算 所以这就是为什么这个答案是…… 情况明显恶化，原因如下： 想象一下从左到右 嗯，我把它复制粘贴到这里了。 答案是三等等，想象一下

### 1:51:16–1:51:39

EN：model having to go from left to right emitting these tokens one at a time it has to say or we're expecting to say the answer is space dollar sign and then right here we're expecting it to basically cram all of the computation of this problem into this single token it has to emit the correct answer three and then once we've emitted the answer three we're expecting it to say all these

中文：模型必须从左到右 它一次发行一个代币 必须说，或者我们预计会说 答案是空格美元符号，然后 我们预计它会在这里发生。 基本上把所有计算都塞进去 这个问题简化成了这一个单一的令牌。 必须发出正确答案三， 然后，一旦我们发出答案三。 我们预计它会说所有这些内容

### 1:51:39–1:52:01

EN：tokens but at this point we've already prod produced the answer and it's already in the context window for all these tokens that follow so anything here is just um kind of post Hawk justification of why this is the answer um because the answer is already created it's already in the token window so it's it's not actually being calculated here um and so if you are answering the

中文：代币，但目前我们已经 prod 给出了答案，那就是 已在上下文窗口中 接下来这些标记什么 这里只是……嗯，算是关于鹰的帖子吧。 解释为什么这是答案 因为答案已经存在了。 它已经在令牌窗口中了，所以是 这里实际上并没有进行计算。 嗯，所以如果你要回答……

### 1:52:01–1:52:23

EN：question directly and immediately you are training the model to to try to basically guess the answer in a single token and that is just not going to work because of the finite amount of computation that happens per token that's why this answer on the right is significantly better because we are Distributing this computation across the answer we're actually getting the model to sort of slowly come to the answer

中文：直接且立即询问你 正在训练模型以尝试 基本上就是凭感觉猜答案。 令牌，但这根本行不通。 因为数量有限 每个令牌发生的计算 这就是为什么右边的答案是 情况明显好转，因为我们是 将此计算分配到 答案是我们实际上正在获取模型 慢慢地得出答案

### 1:52:23–1:52:47

EN：from the left to right we're getting intermediate results we're saying okay the total cost of oranges is four so 30 - 4 is 9 and so we're creating intermediate calculations and each one of these calculations is by itself not that expensive and so we're actually basically kind of guessing a little bit the difficulty that the model is capable of in any single one of these individual tokens and there can never be too much

中文：从左到右，我们依次得到 初步结果我们说可以。 橙子的总成本是4，所以是30。 4 等于 9，所以我们正在创造 中间计算和每一个 这些计算本身并非 价格那么贵，所以我们实际上是 基本上有点靠猜。 该模型所能达到的难度 在这些个人中的任何一个中 代币，而且永远不嫌多。

### 1:52:47–1:53:09

EN：work in any one of these tokens computationally because then the model won't be able to do that later at test time and so we're teaching the model here to spread out its reasoning and to spread out its computation over the tokens and in this way it only has very simple problems in each token and they can add up and then by the time it's near the end it has all the previous

中文：在这些代币中的任何一个中工作 计算上是因为那时模型 之后在测试中将无法做到这一点。 时间，所以我们正在教授这个模型 在这里阐述其理由，并 将其计算分散到 代币，这样它就只有非常多的代币了。 每个代币都有简单的问题，而且它们 积少成多，到那时就…… 临近结尾时，它包含了之前的所有内容。

### 1:53:09–1:53:30

EN：results in its working memory and it's much easier for it to determine that the answer is and here it is three so this is a significantly better label for our computation this would be really bad and is teaching the model to try to do all the computation in a single token and it's really bad so uh that's kind of like an interesting thing to keep in mind is in

中文：这会对其工作记忆产生影响，而且是 这样更容易确定 答案是，这里是三，所以这个 对于我们来说，这是一个明显更好的标签。 计算结果会非常糟糕，而且 正在教模型尝试做所有事情 单个令牌中的计算和 真是 不好，所以，嗯，这有点像…… 值得注意的是，

### 1:53:30–1:53:50

EN：your prompts uh usually don't have to think about it explicitly because uh the people at open AI have labelers and so on that actually worry about this and they make sure that the answers are spread out and so actually open AI will kind of like do the right thing so when I ask this question for chat GPT it's actually going to go very slowly it's going to be like okay let's define our

中文：你的 提示通常不需要思考 明确地谈到这一点，因为呃 OpenAI 的人员有标注员，所以 实际上，我担心这一点。 他们确保答案是 扩散开来，因此实际上开放人工智能将会 有点像做正确的事，所以当 我问这个问题是为了聊天 GPT，它是 实际上会进展得非常缓慢。 会像这样：好吧，让我们来定义一下我们的

### 1:53:50–1:54:10

EN：variables set up the equation and it's kind of creating all these intermediate results these are not for you these are for the model if the model is not creating these intermediate results for itself it's not going to be able to reach three I also wanted to show you that it's possible to be a bit mean to the model uh we can just ask for things so as an example I said I gave it

中文：变量构成方程 它某种程度上创造了所有这些 这些并非中间结果。 这些是为模型准备的，如果该模型 不会创建这些中间体 它本身不会产生任何结果。 能够达到三个我也想 向你展示，有可能有点…… 对于模型来说，我们可以直接询问 举例来说，我给了它

### 1:54:10–1:54:31

EN：the exact same uh prompt and I said answer the question in a single token just immediately give me the answer nothing else and it turns out that for this simple um prompt here it actually was able to do it in single go so it just created a single I think this is two tokens right uh because the dollar sign is its own token so basically this model didn't give me a single token it

中文：同样的提示，我说 请用一个词回答这个问题。 请立即给我答案 仅此而已，结果证明，对于 这里这个简单的提示实际上 能够一次性完成，所以 刚刚创建了一个单独的，我认为这是 两个代币对吧，呃，因为美元 符号本身就是一个标记，所以基本上是这样 模型没有给我任何令牌。

### 1:54:31–1:54:50

EN：gave me two tokens but it still produced the correct answer and it did that in a single forward pass of the network now that's because the numbers here I think are very simple and so I made it a bit more difficult to be a bit mean to the model so I said Emily buys 23 apples and 177 oranges and then I just made the numbers a bit bigger and

中文：给了我两个代币，但它仍然产生了 正确答案是…… 单次前传 现在网络之所以如此，是因为数字。 我觉得这里的东西很简单，所以我 这使得有点难做到…… 对模特来说这意味着什么，所以我说艾米丽买了。 23个苹果和177个橙子，然后我 只是把数字稍微放大了一些。

### 1:54:50–1:55:09

EN：I'm just making it harder for the model I'm asking it to more computation in a single token and so I said the same thing and here it gave me five and five is actually not correct so the model failed to do all of this calculation in a single forward pass of the network it failed to go from the input tokens and then in a single forward pass of the

中文：我只是在给模型增加难度而已。 我要求它在……中进行更多计算 单个代币，所以我说了同样的话。 东西，然后它给了我五和五 实际上并不正确，所以这个模型 未能完成所有这些计算 网络的一次前向传播 无法从输入标记进行操作 然后，在一次向前传球中

### 1:55:09–1:55:32

EN：network single go through the network it couldn't produce the result and then I said okay now don't worry about the the token limit and just solve the problem as usual and then it goes all the intermediate results it simplifies and every one of these intermediate results here and intermediate calculations is much easier for the model and um it sort of it's not too much work per token all

中文：网络单次通过网络 无法得出结果，然后我 他说好了，现在不用担心了。 限制代币数量，然后解决这个问题。 像往常一样，然后一切都变了。 它简化了中间结果，并且 这些中间结果中的每一个 这里以及中间计算是 对于模型来说要容易得多，而且它排序 每个代币的工作量都不算太大

### 1:55:32–1:55:50

EN：of the tokens here are correct and it arises the solution which is seven and I just couldn't squeeze all of this work it couldn't squeeze that into a single forward passive Network so I think that's kind of just a cute example and something to kind of like think about and I think it's kind of again just elucidative in terms of how these uh models work the last thing that I would

中文：这里的一些标记是正确的，而且 由此得出的解是七，而我 实在没办法把所有这些工作都完成。 它无法将所有信息压缩到一个文件中。 前向被动网络，所以我认为 那只是个挺有趣的例子而已。 值得思考一下 我觉得这又有点像…… 阐明这些呃 模型工作是我最不想做的事情。

### 1:55:50–1:56:11

EN：say on this topic is that if I was in practi is trying to actually solve this in my day-to-day life I might actually not uh trust that the model that all the intermediate calculations correctly here so actually probably what I do is something like this I would come here and I would say use code and uh that's because code is one of the possible tools that chachy PD can use and instead

中文：关于这个话题，我想说的是，如果我在…… practi 正在尝试解决这个问题。 在我的日常生活中，我可能真的会 不，呃，相信那个模型，所有的 中间计算结果正确。 所以实际上我大概会这样做 类似这样的事情我就会来这里。 我会说使用代码，嗯，就是这样。 因为代码是可能的选项之一。 chachy PD 可以使用的工具，而不是

### 1:56:11–1:56:31

EN：of it having to do mental arithmetic like this mental arithmetic here I don't fully trust it and especially if the numbers get really big there's no guarantee that the model will do this correctly any one of these intermediates steps might in principle fail we're using neural networks to do mental arithmetic uh kind of like you doing mental arithmetic in your brain it might just like uh screw up some of the

中文：它必须进行心算 比如这种心算，我不会。 完全信任它，尤其是在……的情况下 数字变得非常大，就没有办法了。 保证该模型能够做到这一点 正确地选择这些中间体中的任何一个 原则上，这些步骤可能会失败。 利用神经网络进行心理活动 算术，嗯，有点像你做的那种。 你大脑中的心算可能 就像……搞砸了一些事情

### 1:56:31–1:56:53

EN：intermediate results it's actually kind of amazing that it can even do this kind of mental arithmetic I don't think I could do this in my head but basically the model is kind of like doing it in its head and I don't trust that so I wanted to use tools so you can say stuff like use code and uh I'm not sure what happened there use code and so um like I mentioned there's

中文：中间结果其实挺好的 令人惊叹的是它竟然能做到这种程度 我不认为我擅长心算。 我可以在脑子里完成这件事，但基本上 这种模式有点像在……中做这件事 它的头，我不信任它，所以我 想用工具让你能说点什么 像使用 代码，呃，我不确定发生了什么。 用途 代码，就像我刚才提到的那样，有

### 1:56:53–1:57:14

EN：a special tool and the uh the model can write code and I can inspect that this code is correct and then uh it's not relying on its mental arithmetic it is using the python interpreter which is a very simple programming language to basically uh write out the code that calculates the result and I would personally trust this a lot more because this came out of a Python program which

中文：一种特殊工具，以及该模型可以 编写代码，我可以检查这一点。 代码一开始是正确的，然后……呃，它又不对。 它依靠心算能力 使用 Python 解释器，它是一个 非常简单的编程语言 基本上就是把代码写出来。 计算结果，我会 我个人更信任这个，因为 这是由一个Python程序生成的，该程序

### 1:57:14–1:57:36

EN：I think has a lot more correctness guarantees than the mental arithmetic of a language model uh so just um another kind of uh potential hint that if you have these kinds of problems uh you may want to basically just uh ask the model to use the code interpreter and just like we saw with the web search the model has special uh kind of tokens for calling uh like it will not actually

中文：我认为这样更准确。 比心算更有保障 语言模型，呃，所以只是……另一个 这有点像是在暗示，如果你 你可能会遇到这类问题。 我基本上只是想问问模特。 使用代码解释器，只需 就像我们在网络搜索中看到的那样…… 该模型具有特殊的令牌类型 打电话好像不会真的发生

### 1:57:36–1:57:55

EN：generate these tokens from the language model it will write the program and then it actually sends that program to a different sort of part of the computer that actually just runs that program and brings back the result and then the model gets access to that result and can tell you that okay the cost of each apple is seven um so that's another kind of tool and I

中文：从语言中生成这些词元 模型会编写程序，然后 它实际上将该程序发送到 计算机的不同部件 实际上，它只是运行那个程序而已。 返回结果，然后 模型可以访问该结果并可以 告诉你每个的成本是多少。 苹果是七 嗯，这是另一种工具，而且我

### 1:57:55–1:58:18

EN：would use this in practice for yourself and it's um yeah it's just uh less error prone I would say so that's why I called this section models need tokens to think distribute your competition across many tokens ask models to create intermediate results or whenever you can lean on tools and Tool use instead of allowing the models to do all of the stuff in their memory so if they try to do it all

中文：我会把它运用到自己的实践中。 嗯，是的，错误率确实更低。 我觉得他容易上当，所以我才打电话的。 本节模型需要令牌才能思考 将您的竞争对手分散到多个方面 令牌要求模型创建中间体 结果或任何时候你可以依靠 工具和工具使用，而不是允许 这些模型可以完成所有这些工作 他们的记忆力不好，所以如果他们试图完成所有事情的话。

### 1:58:18–1:58:38

EN：in their memory I don't fully trust it and prefer to use tools whenever possible I want to show you one more example of where this actually comes up and that's in counting so models actually are not very good at counting for the exact same reason you're asking for way too much in a single individual token so let me show you a simple example of that um how many dots are

中文：在他们的记忆中，我并不完全信任它。 而且我更喜欢在任何时候都使用工具。 或许我还想再给你看一个。 举个例子，这种情况确实会发生。 这就是模型计数的一部分。 实际上他们不太擅长数数 原因跟你问的完全一样。 一个人承担了太多责任 所以让我给你展示一个简单的令牌。 举个例子，嗯，有多少个点？

### 1:58:38–1:58:58

EN：below and then I just put in a bunch of dots and Chach says there are and then it just tries to solve the problem in a single token so in a single token it has to count the number of dots in its context window um and it has to do that in the single forward pass of a network and a single forward pass of a network as we talked

中文：下面，然后我就放了一堆 点，查奇说那里有，然后 它只是尝试用一种方法解决问题。 单个令牌，因此在单个令牌中它有 计算其上的点数 上下文窗口 嗯，而且它必须在单曲中做到这一点。 网络的前向传播和单个 正如我们刚才所说，网络的前向传播

### 1:58:58–1:59:22

EN：about there's not that much computation that can happen there just think of that as being like very little competation that happens there so if I just look at what the model sees let's go to the LM go to tokenizer it sees uh this how many dots are below and then it turns out that these dots here this group of I think 20 dots is a single token and then this group of whatever it

中文：计算量其实并不大。 那种事在那里可能会发生，想想看。 几乎没有竞争对手 那里就会发生这种情况，所以如果我只看 模型看到的景象，我们去看看LM（着陆器）。 去分词器，它看到了呃 下面有多少个点？然后它 原来这些点在这里 我认为一组20个点是一个 令牌，然后是这组任何东西

### 1:59:22–1:59:45

EN：is is another token and then for some reason they break up as this so I don't actually this has to do with the details of the tokenizer but it turns out that these um the model basically sees the token ID this this this and so on and then from these token IDs it's expected to count the number and spoiler alert is not 161 it's actually I believe

中文：这是另一个标记，然后对于某些 他们分手的原因是这个，所以我不这么认为。 实际上，这与细节有关。 分词器，但结果却是…… 这些模型基本上可以看到 令牌 ID 这个 这个 这个 等等 然后根据这些令牌 ID 可以预期 计算数字，剧透警告是 不是161，实际上我认为是

### 1:59:45–2:00:08

EN：177 so here's what we can do instead uh we can say use code and you might expect that like why should this work and it's actually kind of subtle and kind of interesting so when I say use code I actually expect this to work let's see okay 177 is correct so what happens here is I've actually it doesn't look like it but I've broken down the problem into a

中文：177 所以我们可以这样做： 我们可以说使用代码，你可能会期望 就像，为什么这种方法会奏效？ 实际上有点微妙，有点 很有意思，所以当我说使用代码时， 实际上，我预计这会奏效，让我们拭目以待。 好的，177 是正确的，那么接下来会发生什么呢？ 实际上，看起来不像。 但我已经把问题分解成……

### 2:00:08–2:00:29

EN：problems that are easier for the model I know that the model can't count it can't do mental counting but I know that the model is actually pretty good at doing copy pasting so what I'm doing here is when I say use code it creates a string in Python for this and the task of basically copy pasting my input here to here is very simple because for the

中文：对于 I 型模型来说，问题更容易解决。 要知道，这个模型不能计数，它不能 我会进行心算，但我知道 该模型实际上非常擅长做 复制粘贴，所以我现在做的是…… 我说使用代码，它会创建一个字符串。 用 Python 来实现这个任务 基本上就是把我输入的内容复制粘贴到这里 这里很简单，因为

### 2:00:29–2:00:53

EN：model um it sees this string of uh it sees it as just these four tokens or whatever it is so it's very simple for the model to copy paste those token IDs and um kind of unpack them into Dots here and so it creates this string and then it calls python routine. count and then it comes up with the correct answer so the python interpreter is doing the

中文：模型嗯，它看到了这串呃它 将其视为这四个代币或 不管是什么，都很简单。 用于复制粘贴这些令牌 ID 的模型 然后，嗯，把它们拆解成点状物。 所以它在这里创建了这个字符串。 然后它调用 Python 例程。计数和 然后它得出了正确答案 所以，Python解释器正在执行以下操作：

### 2:00:53–2:01:15

EN：counting it's not the models mental arithmetic doing the counting so it's again a simple example of um models need tokens to think don't rely on their mental arithmetic and um that's why also the models are not very good at counting if you need them to do counting tasks always ask them to lean on the tool now the models also have many other little cognitive deficits here and there and

中文：计算一下，这不是模型的心理状态。 算术运算进行计数，所以它是 再举一个简单的例子，说明模型需要 代币思考不要依赖它们 心算，嗯，这就是原因。 这些模型在计数方面不太擅长。 如果你需要他们进行计数任务 现在就让他们依靠这个工具。 这些模型还有许多其他小功能 认知能力存在一些缺陷，

## 14. tokenization revisited: models struggle with spelling（2:01:11–2:04:53）

### 2:01:15–2:01:33

EN：these are kind of like sharp edges of the technology to be kind of aware of over time so as an example the models are not very good with all kinds of spelling related tasks they're not very good at it and I told you that we would loop back around to tokenization and the reason to do for this is that the models they don't see the characters they see

中文：这些有点像锋利的边缘 这项技术需要有所了解 随着时间的推移，例如模型 不太擅长处理各种事情 与拼写相关的任务，他们不太擅长。 我擅长这个，我告诉过你我们会 循环回到标记化和 这样做的原因是模型 他们看不到他们所看到的角色

### 2:01:33–2:01:56

EN：tokens and they their entire world is about tokens which are these little text chunks and so they don't see characters like our eyes do and so very simple character level tasks often fail so for example uh I'm giving it a string ubiquitous and I'm asking it to print only every third character starting with the first one so we start with U and then we should go every third so every

中文：代币，以及他们的整个世界 关于令牌，也就是这些小文本 块，所以他们看不到字符 就像我们的眼睛一样，非常简单。 角色级任务经常失败，因此 例如，我给它一个字符串 无处不在，我要求它打印 只有每三个以……开头的字符 第一个，所以我们从U开始， 那么我们应该每隔三天进行一次，所以每

### 2:01:56–2:02:19

EN：so 1 2 3 Q should be next and then Etc so this I see is not correct and again my hypothesis is that this is again Dental arithmetic here is failing number one a little bit but number two I think the the more important issue here is that if you go to Tik tokenizer and you look at ubiquitous we see that it is three tokens right so you

中文：所以接下来应该是 1 2 3 Q，然后是等等。 所以我觉得这个说法不正确，而且…… 我的假设是，这又是…… 这里的牙科算术是失败的数字 一个有点，但第二个我觉得…… 这里更重要的问题是 如果你去Tik 分词器，你看看无处不在的我们 你看，是三个代币，对吧？

### 2:02:19–2:02:39

EN：and I see ubiquitous and we can easily access the individual letters because we kind of see them and when we have it in the working memory of our visual sort of field we can really easily index into every third letter and I can do that task but the models don't have access to the individual letters they see this as these three tokens and uh remember these models are trained from scratch on the

中文：我看到它无处不在，而且我们很容易就能 因为我们能够访问单个信件，所以我们 有点像看到它们，当我们拥有它们的时候 我们视觉类型的工作记忆 我们可以很容易地对字段进行索引 每隔三个字母，我可以做到。 任务，但模型无法访问 他们认为这些字母是 这三个代币，还有，记住这些 模型从头开始训练

### 2:02:39–2:02:59

EN：internet and all these token uh basically the model has to discover how many of all these different letters are packed into all these different tokens and the reason we even use tokens is mostly for efficiency uh but I think a lot of people areed interested to delete tokens entirely like we should really have character level or bite level models it's just that that would create very long sequences and people don't

中文：互联网和所有这些代币呃 基本上，该模型必须发现如何 这些不同的字母有很多是 所有这些不同的代币都包含了 我们使用令牌的原因是 主要是为了提高效率，但我认为 很多人都有兴趣删除 代币完全就像我们应该做的那样 角色等级或咬合等级 模型，只是那样会创建 非常长的序列，人们不会

### 2:02:59–2:03:18

EN：know how to deal with that right now so while we have the token World any kind of spelling tasks are not actually expected to work super well so because I know that spelling is not a strong suit because of tokenization I can again Ask it to lean On Tools so I can just say use code and I would again expect this to work because the task of copy pasting

中文：现在知道该如何处理这件事了。 虽然我们拥有任何类型的代币世界 拼写任务实际上并非如此 预计效果会非常好，因为我 我知道我的拼写能力不太好。 由于分词技术，我可以再次提问 它依靠工具，所以我就可以这么说了。 使用代码，我再次期待这一点。 因为复制粘贴这项任务需要工作

### 2:03:18–2:03:47

EN：ubiquitous into the python interpreter is much easier and then we're leaning on python interpreter to manipulate the characters of this string so when I say use code ubiquitous yes it indexes into every third character and the actual truth is u2s uqs uh which looks correct to me so um again an example of spelling related tasks not working very well a very famous example of that recently is how

中文：普遍存在于 Python 解释器中 这样容易得多，然后我们就可以依靠它了。 使用 Python 解释器来操作 这个字符串的字符，所以当我说 使用 代码 无处不在，是的，它索引到每一个 第三个角色和真相是 u2s uqs 嗯，在我看来这似乎是正确的，所以嗯 又一个例子与拼写相关 任务运行不太顺利，非常 最近一个著名的例子是……

### 2:03:47–2:04:06

EN：many R are there in strawberry and this went viral many times and basically the models now get it correct they say there are three Rs in Strawberry but for a very long time all the state-of-the-art models would insist that there are only two RS in strawberry and this caused a lot of you know Ruckus because is that a word I think so because um it just kind

中文：草莓中有很多R，而且 多次在网络上疯传，基本上 他们说，现在的模型都能正确显示这一点了。 草莓有三个R，但对于一个 很长一段时间以来，所有最先进的技术 模型会坚持认为只有 草莓中含有两个RS，这导致了 你们很多人都知道Ruckus，因为那是…… 我觉得是这样，因为嗯，它就是那种感觉。

### 2:04:06–2:04:27

EN：of like why are the models so brilliant and they can solve math Olympiad questions but they can't like count RS in strawberry and the answer for that again is I've got built up to it kind of slowly but number one the models don't see characters they see tokens and number two they are not very good at counting and so here we are combining the difficulty of seeing the characters

中文：比如，为什么这些模型如此出色？ 他们能够解决数学奥林匹克竞赛题 问题，但他们不能像计数RS那样提问 草莓味的，以及这个问题的答案 再说一遍，我已经为此做好了准备。 缓慢但第一，模型们没有 他们看到字符，就看到了代币和 第二，他们不太擅长 计数，所以我们在这里合并 难以看清人物

### 2:04:27–2:04:48

EN：with the difficulty of counting and that's why the models struggled with this even though I think by now honestly I think open I may have hardcoded the answer here or I'm not sure what they did but um uh but this specific query now works so models are not very good at spelling and there there's a bunch of other little sharp edges and I don't want to go into all of them I just want to show

中文：计数困难 这就是为什么这些模型难以应对 虽然我现在觉得…… 我认为开放的，我可能已经硬编码了。 请在此处回答，否则我不确定他们是什么意思。 确实，但是嗯，呃，但是这个具体的查询 现在有效 所以模特们的拼写能力不太好。 那里还有很多其他的 边缘有些锋利，我不想…… 我只想展示所有这些。

### 2:04:48–2:05:05

EN：you a few examples of things to be aware of and uh when you're using these models in practice I don't actually want to have a comprehensive analysis here of all the ways that the models are kind of like falling short I just want to make the point that there are some Jagged edges here and there and we've discussed a few of them and a few of them make

中文：以下是一些需要注意的事项示例。 以及，当你在使用这些模型时 实际上我并不想这样做。 这里有一份全面的分析报告。 这些模型的所有方式都有些…… 就像未能达到预期目标一样，我只想…… 关键在于有一些锯齿状的东西 这里那里都有一些边缘，我们已经讨论过了。 他们中的一些人，他们中的一些人制造

## 15. jagged intelligence（2:04:53–2:07:28）

### 2:05:05–2:05:23

EN：sense but some of them also will just not make as much sense and they're kind of like you're left scratching your head even if you understand in- depth how these models work and and good example of that recently is the following uh the models are not very good at very simple questions like this and uh this is shocking to a lot of people because these math uh these problems can solve

中文：有道理，但他们中的一些人也会这么做。 不太有道理，而且他们很友善。 就像你百思不得其解一样 即使你深入了解了如何 这些模型有效，而且是一个很好的例子。 最近的情况如下： 模型在非常简单的场景下表现并不好。 像这样的问题，还有这个…… 这令很多人感到震惊，因为 这些数学问题可以解决

### 2:05:23–2:05:49

EN：complex math problems they can answer PhD grade physics chemistry biology questions much better than I can but sometimes they fall short in like super simple problems like this so here we go 9.11 is bigger than 9.9 and it justifies it in some way but obviously and then at the end okay it actually it flips its decision later so um I don't believe that this is very reproducible sometimes

中文：他们能够回答复杂的数学问题 博士级别的物理、化学和生物学 问的问题比我好得多，但是 有时他们会像超级英雄一样表现不佳。 像这样的简单问题，我们开始吧。 9.11 比 9.9 大，这足以证明其合理性。 在某种程度上是这样，但显然，然后在 结尾好吧，它实际上翻转了。 稍后再做决定，所以嗯，我不相信 这种情况有时很容易重现。

### 2:05:49–2:06:12

EN：it flips around its answer sometimes gets it right sometimes get it get it wrong uh let's try again okay even though it might look larger okay so here it doesn't even correct itself in the end if you ask many times sometimes it gets it right too but how is it that the model can do so great at Olympiad grade problems but then fail on very simple problems like

中文：它的答案有时会发生转变。 有时候能做对，明白了，明白了 错了，呃，我们试试。 好吧，即使它看起来可能…… 更大一些，所以这里甚至都没有。 如果你问，它最终会自行纠正。 很多时候，它都能做对。 但是，这个模型是如何做到的呢？ 非常擅长奥林匹克级别的题目，但是 然后连一些非常简单的问题都解决不了，比如

### 2:06:12–2:06:33

EN：this and uh I think this one is as I mentioned a little bit of a head scratcher it turns out that a bunch of people studied this in depth and I haven't actually read the paper uh but what I was told by this team was that when you scrutinize the activations inside the neural network when you look at some of the features and what what features turn on or off and what neurons

中文：这个，还有，嗯，我觉得这个就像我 稍微提到了头部 刮刮乐，结果发现一堆 人们对此进行了深入研究，而我 我还没看过那篇论文呢，呃…… 这个团队告诉我的是： 当你仔细查看激活信息时 当你观察神经网络内部时 在某些功能方面以及什么 功能开启或关闭以及哪些神经元

### 2:06:33–2:06:58

EN：turn on or off uh a bunch of neurons inside the neural network light up that are usually associated with Bible verses U and so I think the model is kind of like reminded that these almost look like Bible verse markers and in a bip verse setting 9.11 would come after 99.9 and so basically the model somehow finds it like cognitively very distracting that in Bible verses 9.11 would be

中文：打开或关闭一大堆神经元 神经网络内部会亮起。 通常与圣经经文相关 所以我觉得这个模型有点像 就像提醒我，这些几乎看起来 就像圣经经文标记和在bip中 诗节设定9.11将在99.9之后。 所以基本上，该模型以某种方式找到了 它就像是在认知上非常分散注意力。 圣经第9章第11节中提到的就是

### 2:06:58–2:07:19

EN：greater um even though here it's actually trying to justify it and come up to the answer with a math it still ends up with the wrong answer here so it basically just doesn't fully make sense and it's not fully understood and um there's a few Jagged issues like that so that's why treat this as a as what it is which is a St stochastic system that is

中文：更大的嗯，即使在这里是 实际上，我试图为之辩解，然后…… 直到用数学方法得出答案为止，它仍然 结果这里得出了错误的答案，所以 基本上就是说不通。 而且它还没有被完全理解，嗯 像这样的 Jagged 问题还有一些。 所以，请把它当作它本来的样子来看待。 这是一个St随机系统，即

### 2:07:19–2:07:40

EN：really magical but that you can't also fully trust and you want to use it as a tool not as something that you kind of like letter rip on a problem and copypaste the results okay so we have now covered two major stages of training of large language models we saw that in the first stage this is called the pre-training stage we are basically training on internet documents and when

中文：真的很神奇，但你也不能这么做 完全信任，并且你想把它用作…… 工具，而不是某种你用来……的东西 就像撕开信件一样，这是一个问题。 复制粘贴结果，好的，所以我们有 目前已涵盖两个主要训练阶段 在大型语言模型中，我们看到了这一点。 第一阶段被称为 预备训练阶段我们基本上是 关于互联网文档的培训以及何时

## 16. supervised finetuning to reinforcement learning（2:07:28–2:14:42）

### 2:07:40–2:08:02

EN：you train a language model on internet documents you get what's called a base model and it's basically an internet document simulator right now we saw that this is an interesting artifact and uh this takes many months to train on thousands of computers and it's kind of a lossy compression of the internet and it's extremely interesting but it's not directly useful because we don't want to sample internet documents we want to ask

中文：你在互联网上训练一个语言模型 你收到的文件叫做基本文件。 模型，它基本上是一个互联网 我们刚才看到的文档模拟器 这是一件有趣的文物，呃…… 这需要几个月的训练时间。 成千上万台电脑，这有点…… 互联网的有损压缩和 它非常有趣，但它并非如此。 直接有用，因为我们不想 我们想询问的互联网文档示例

### 2:08:02–2:08:27

EN：questions of an AI and have it respond to our questions so for that we need an assistant and we saw that we can actually construct an assistant in the process of a post training and specifically in the process of supervised fine-tuning as we call it so in this stage we saw that it's algorithmically identical to pre-training nothing is going to change the only thing that changes is the data

中文：向人工智能提出问题并让它回答 为了回答我们的问题，我们需要一个 助理，我们看到我们可以 实际上构建了一个助手 帖子处理过程 培训，尤其是在过程中 监督式微调，我们称之为 所以在这个阶段我们看到，它是 算法上与 训练前一切都不会改变 唯一改变的是数据。

### 2:08:27–2:08:57

EN：set so instead of Internet documents we now want to create and curate a very nice data set of conversations so we want Millions conversations on all kinds of diverse topics between a human and an assistant and fundamentally these conversations are created by humans so humans write the prompts and humans write the ideal response responses and they do that based on labeling documentations now in the modern stack

中文：这样一来，我们就不用互联网文档了。 现在想创建和策划一个非常 我们拥有不错的对话数据集。 想要进行数百万次关于各种话题的对话 人类与人类之间各种话题的讨论 助理，以及从根本上说这些 对话是由人类创造的，所以 人类编写提示语，人类 写出理想的回应和 他们这样做是基于标签的。 现代技术栈中的文档现已更新。

### 2:08:57–2:09:17

EN：it's not actually done fully and manually by humans right they actually now have a lot of help from these tools so we can use language models um to help us create these data sets and that's done extensively but fundamentally it's all still coming from Human curation at the end so we create these conversations that now becomes our data set we fine tune on it or continue training on it

中文：实际上还没有完全完成， 人工操作，没错，他们确实如此 现在这些工具给了我很多帮助。 所以我们可以利用语言模型来提供帮助 我们创建了这些数据集，就是这样。 虽然已经做了很多，但从根本上来说，它是 所有内容仍然来自人工筛选 最后，我们才发起这些对话。 现在，它就成了我们的数据集，我们很好。 收听或继续训练

### 2:09:17–2:09:38

EN：and we get an assistant and then we kind of shifted gears and started talking about some of the kind of cognitive implications of what this assistant is like and we saw that for example the assistant will hallucinate if you don't take some sort of mitigations towards it so we saw that hallucinations would be common and then we looked at some of the mitigations of those hallucinations and

中文：然后我们找了个助手，然后我们…… 话锋一转，开始说话 关于某些类型的认知 这位助手意味着什么 比如，我们看到，例如…… 如果你不这样做，助手会出现幻觉。 采取一些缓解措施来应对这种情况。 所以我们看到幻觉会是 然后我们看了一些常见的…… 缓解这些幻觉和

### 2:09:38–2:09:57

EN：then we saw that the models are quite impressive and can do a lot of stuff in their head but we saw that they can also Lean On Tools to become better so for example we can lo lean on a web search in order to hallucinate less and to maybe bring up some more um recent information or something like that or we can lean on tools like code interpreter

中文：然后我们看到这些模型相当 令人印象深刻，而且能做很多事情 他们的头，但我们看到他们也可以 依靠工具来变得更好 例如，我们可以依靠网络搜索。 为了减少幻觉，并且 或许可以提一些最近的情况。 信息或类似的东西，或者我们 可以依靠代码解释器之类的工具

### 2:09:57–2:10:19

EN：so the code can so the llm can write some code and actually run it and see the results so these are some of the topics we looked at so far um now what I'd like to do is I'd like to cover the last and major stage of this Pipeline and that is reinforcement learning so reinforcement learning is still kind of thought to be under the umbrella of posttraining uh

中文：所以代码可以这样写，LLM 就可以写。 写一些代码，然后实际运行一下看看。 这 结果如下，以上是一些主题。 我们目前为止都看过了，嗯，现在我想要什么？ 我想做的就是涵盖最后一个和 该管道的主要阶段是…… 强化学习，因此强化 人们仍然认为学习是一种…… 在培训后……的框架下

### 2:10:19–2:10:44

EN：but it is the last third major stage and it's a different way of training language models and usually follows as this third step so inside companies like open AI you will start here and these are all separate teams so there's a team doing data for pre-training and a team doing training for pre-training and then there's a team doing all the conversation generation in a in a different team that is kind of doing the

中文：但这是最后一个主要阶段，而且 这是一种不同的训练方式。 语言模型通常遵循以下规则： 第三步，也就是公司内部的类似步骤 OpenAI，你将从这里开始，以及这些 都是独立的团队，所以有一个团队 为预训练收集数据和一个团队 进行岗前培训，然后 有一个团队负责所有的事情 在 a 中生成对话 另一个团队正在做类似的事情

### 2:10:44–2:11:03

EN：supervis fine tuning and there will be a team for the reinforcement learning as well so it's kind of like a handoff of these models you get your base model the then you find you need to be an assistant and then you go into reinforcement learning which we'll talk about uh now so that's kind of like the major flow and so let's now focus on reinforcement learning the last major

中文：监督微调，并且将会有一个 团队负责强化学习 所以这有点像交接…… 这些型号中，您将获得一个基本型号。 然后你会发现你需要成为一名 助理，然后你进入 我们稍后会谈到强化学习。 关于呃 所以，这有点像是主要问题。 流程，所以现在让我们专注于…… 强化学习是最后一个主要学习成果。

### 2:11:03–2:11:21

EN：stage of training and let me first actually motivate it and why we would want to do reinforcement learning and what it looks like on a high level so I would now like to try to motivate the reinforcement learning stage and what it corresponds to with something that you're probably familiar with and that is basically going to school so just like you went to school to become um

中文：训练阶段，首先让我…… 实际上，要阐明其动机以及我们为什么要这样做。 想做强化学习， 从宏观角度来看，它看起来是什么样的呢？ 现在想尝试激励 强化学习阶段及其内容 与某事物相对应 你可能很熟悉这一点。 基本上就是去上学，所以就…… 就像你上学是为了成为……

### 2:11:21–2:11:46

EN：really good at something we want to take large language models through school and really what we're doing is um we're um we have a few paradigms of ways of uh giving them knowledge or transferring skills so in particular when we're working with textbooks in school you'll see that there are three major kind of uh pieces of information in these textbooks three classes of information the first thing you'll see is you'll see

中文：非常擅长我们想要学习的某项技能 通过学校和大型语言模型 我们真正要做的是…… 我们有一些方法范式，呃…… 赋予他们知识或转移 技能，尤其是在我们……的时候 在学校里使用教科书时，你会 可以看出，主要有三种类型 呃，这些信息片段 教科书分为三类信息 你首先会看到的是……

### 2:11:46–2:12:05

EN：a lot of exposition um and by the way this is a totally random book I pulled from the internet I I think it's some kind of an organic chemistry or something I'm not sure uh but the important thing is that you'll see that most of the text most of it is kind of just like the meat of it is exposition it's kind of like background knowledge Etc as you are reading through the words

中文：很多说明，嗯，顺便说一句 这是我随机抽取的一本书。 我从网上看到的，我觉得是一些 某种有机化学或 有些事我不太确定，呃，但是 重要的是你会看到这一点。 大部分文本都有些…… 就像它的核心是阐述一样 这有点像背景知识 等等，当你阅读这些文字的时候

### 2:12:05–2:12:28

EN：of this Exposition you can think of that roughly as training on that data so um and that's why when you're reading through this stuff this background knowledge and this all this context information it's kind of equivalent to pre-training so it's it's where we build sort of like a knowledge base of this data and get a sense of the topic the next major kind of information that you

中文：你可以把这次博览会看作是…… 大致相当于用这些数据进行训练，所以嗯 所以当你阅读的时候 通过这些东西，这个背景 知识以及所有这些背景 它与信息有点类似 预备训练，所以这是我们构建的地方。 有点像这方面的知识库。 收集数据并了解主题。 下一个重要的信息类型是……

### 2:12:28–2:12:52

EN：will see is these uh problems and with their worked Solutions so basically a human expert in this case uh the author of this book has given us not just a problem but has also worked through the solution and the solution is basically like equivalent to having like this ideal response for an assistant so it's basically the expert is showing us how to solve the problem in it's uh kind of

中文：我们将会看到这些问题，以及与 他们的解决方案基本上是 本案中的人类专家，呃，就是作者。 这本书带给我们的不仅仅是 问题，但也已经解决了 解决方案，基本上就是 就像这样，相当于拥有这样的能力 对于助理来说，这是理想的回答。 基本上，这位专家正在向我们展示如何 解决这个问题有点……

### 2:12:52–2:13:19

EN：like um in its full form so as we are reading the solution we are basically training on the expert data and then later we can try to imitate the expert um and basically um that's that roughly correspond to having the sft model that's what it would be doing so basically we've already done pre-training and we've already covered this um imitation of experts and how they solve these problems and the third

中文：就像嗯，它的完整形式，所以我们是 阅读解决方案，我们基本上是 利用专家数据进行训练，然后 之后我们可以尝试模仿专家。 嗯，基本上就是这样。 对应于具有 sft 模型 它就是这么做的。 基本上我们已经完成了 预备训练，我们已经涵盖了 这种模仿专家的方式 他们解决了这些问题，还有第三个问题。

### 2:13:19–2:13:42

EN：stage of reinforcement learning is basically the practice problems so sometimes you'll see this is just a single practice problem here but of course there will be usually many practice problems at the end of each chapter in any textbook and practice problems of course we know are critical for learning because what are they getting you to do they're getting you to practice uh to practice yourself and discover ways of solving these problems

中文：强化学习阶段是 基本上就是练习题。 有时你会发现这只是一个 这里只有一个练习题，但是 当然，通常会有很多。 每节课末尾都有练习题。 任何教科书中的章节和练习 我们当然知道这些问题至关重要。 为了学习，因为它们是什么？ 让你做他们想让你做的事 练习，呃，练习自己， 找出解决这些问题的方法

### 2:13:42–2:14:02

EN：yourself and so what you get in a practice problem is you get a problem description but you're not given the solution but you are given the final answer answer usually in the answer key of the textbook and so you know the final answer that you're trying to get to and you have the problem statement but you don't have the solution you are trying to practice the solution you're

中文：你自己，以及你从中得到什么 练习题就是你遇到一个问题 描述，但你没有得到 但你得到的是最终的解决方案。 答案通常在答案表中。 教科书上的内容，所以你知道 你想要得到的最终答案 到此，你就有了问题陈述。 但你并没有找到解决办法。 尝试练习你正在使用的解决方案

### 2:14:02–2:14:25

EN：trying out many different things and you're seeing what gets you to the final solution the best and so you're discovering how to solve these problems so and in the process of that you're relying on number one the background information which comes from pre-training and number two maybe a little bit of imitation of human experts and you can probably try similar kinds of solutions and so on so we've done

中文：尝试了很多不同的事情 你现在看到的是让你走到最后的因素。 最佳解决方案，所以你是 探索如何解决这些问题 所以，在这个过程中，你 依靠第一点背景 信息来源 预备训练，第二点可能是 对人类专家进行一些模仿 你或许可以尝试类似的类型 解决方案等等，我们已经完成了

### 2:14:25–2:14:46

EN：this and this and now in this section we're going to try to practice and so we're going to be given prompts we're going to be given Solutions U sorry the final answers but we're not going to be given expert Solutions we have to practice and try stuff out and that's what reinforcement learning is about okay so let's go back to the problem that we worked with previously just so

中文：这个和这个，现在在这个部分 我们打算尝试练习一下，所以 我们将收到一些提示。 将会给出解决方案 U 抱歉 最终答案尚未确定，但我们不会…… 鉴于专家提供的解决方案，我们必须 练习和尝试，就是这样。 强化学习是什么 好的，我们回到这个问题。 我们之前合作过的那个人就是这样

## 17. reinforcement learning（2:14:42–2:27:47）

### 2:14:46–2:15:06

EN：we have a concrete example to talk through as we explore sort of the topic here so um I'm here in the Teck tokenizer because I'd also like to well I get a text box which is useful but number two I want to remind you again that we're always working with onedimensional token sequences and so um I actually like prefer this view because this is like the native view of the llm

中文：我们有一个具体的例子可以讨论。 在我们探讨这个话题的过程中 我现在在泰克公司。 分词器，因为我也想…… 我会得到一个文本框，这很有用，但是 第二点，我想再次提醒你。 我们一直都在与……合作 一维标记序列等等 我其实更喜欢这种观点，因为 这就像LLM的原生视图一样

### 2:15:06–2:15:31

EN：if that makes sense like this is what it actually sees it sees token IDs right okay so Emily buys three apples and two oranges each orange is $2 the total cost of all the fruit is $13 what is the cost of each apple and what I'd like to what I like you to appreciate here is these are like four possible candidate Solutions as an example and they all reach the answer

中文：如果这样说你能理解的话，那就是它 实际上它看到了令牌 ID，对吧？ 好的，艾米丽买了三个苹果和两个 每个橙子2美元，总成本 所有水果的总价是 13 美元，那么成本是多少？ 每个苹果 以及我希望你做的。 这里值得注意的是，这就像四个 可能的候选解决方案 例如，他们都找到了答案。

### 2:15:31–2:15:54

EN：three now what I'd like you to appreciate at this point is that if I am the human data labeler that is creating a conversation to be entered into the training set I don't actually really know which of these conversations to um to add to the data set some of these conversations kind of set up a system equations some of them sort of like just talk through it in

中文：第三，现在我想请你做什么 此时此刻我最清楚的是，如果我是 创建数据的人工标注员 即将展开的对话 训练集我其实不太 知道是哪一种 对话是为了补充数据 把其中一些对话设定成某种…… 建立一些系统方程 就像直接聊聊一样。

### 2:15:54–2:16:15

EN：English and some of them just kind of like skip right through to the solution um if you look at chbt for example and you give it this question it defines a system of variables and it kind of like does this little thing what we have to appreciate and uh differentiate between though is um the first purpose of a solution is to reach the right answer of course we want to

中文：英语，还有一些人只是有点…… 就像直接跳到…… 解决方案是，如果你看一下 chbt 的话 举个例子，你给它这个问题 定义了一个变量系统，并且 有点像这个小东西会做什么 我们必须懂得欣赏，呃…… 区分两者是嗯…… 解决方案的首要目的是达到 我们当然想要正确的答案。

### 2:16:15–2:16:33

EN：get the final answer three that is the that is the important purpose here but there's kind of like a secondary purpose as well where here we are also just kind of trying to make it like nice uh for the human because we're kind of assuming that the person wants to see the solution they want to see the intermediate steps we want to present it nicely Etc so there are two separate

中文：得到最终答案三，那就是 这才是这里的重要目的，但是 这有点像是次要目的 我们在这里也只是友善而已。 试图让它变得像……嗯…… 因为我们某种程度上是在假设人类。 这个人想看 他们希望看到的解决方案 我们想展示的中间步骤 很好等等，所以有两个独立的

### 2:16:33–2:16:57

EN：things going on here number one is the presentation for the human but number two we're trying to actually get the right answer um so let's for the moment focus on just reaching the final answer if we're only care if we only care about the final answer then which of these is the optimal or the best prompt um sorry the best solution for the llm to reach the right

中文：这里发生的事情第一点是…… 人类的呈现方式，但数量 我们正在努力争取获得两个…… 正确答案，嗯，那么我们暂时…… 只需专注于得出最终答案即可。 如果我们只关心如果我们只关心 那么最终答案是以下哪一项呢？ 最佳或最合适的提示，嗯，抱歉。 LLM 达到最佳解决方案 右

### 2:16:57–2:17:19

EN：answer um and what I'm trying to get at is we don't know me as a human labeler I would not know which one of these is best so as an example we saw earlier on when we looked at um the token sequences here and the mental arithmetic and reasoning we saw that for each token we can only spend basically a finite number of finite amount of compute here that is not very

中文：回答一下，嗯，还有我想表达的意思。 我们并不了解我作为人类标签制作者的能力。 不知道这其中哪一个是 最好就像我们之前看到的例子那样。 当我们审视 嗯，这里的标记序列和 我们看到的心算和推理能力 每个代币我们只能花费 基本上是有限数量的有限 这里的计算量并不大。

### 2:17:19–2:17:36

EN：large or you should think about it that way way and so we can't actually make too big of a leap in any one token is is maybe the way to think about it so as an example in this one what's really nice about it is that it's very few tokens so it's going to take us very short amount of time to get to the answer but right

中文：大点，或者你应该考虑一下。 太远了，所以我们实际上无法做到 任何单一代币的跨度都太大了。 或许可以这样想： 举个例子，这个例子真正吸引人的地方是什么？ 问题在于代币数量非常少。 这只需要我们很短的时间。 需要时间才能找到答案，但没错

### 2:17:37–2:17:56

EN：here when we're doing 30 - 4 IDE 3 equals right in this token here we're actually asking for a lot of computation to happen on that single individual token and so maybe this is a bad example to give to the llm because it's kind of incentivizing it to skip through the calculations very quickly and it's going to actually make up mistakes make mistakes in this mental arithmetic uh so

中文：这里我们正在进行 30 - 4 IDE 3 的操作。 等于这里这个标记中的正确位置 实际上需要大量的计算 碰巧遇到那个人 令牌，所以这或许是个不好的例子。 捐给法学硕士，因为它有点像 激励它跳过 计算速度非常快，而且正在进行中 要真正弥补错误 这次心算出错了，呃……

### 2:17:56–2:18:16

EN：maybe it would work better to like spread out the spread it out more maybe it would be better to set it up as an equation maybe it would be better to talk through it we fundamentally don't know and we don't know because what is easy for you or I as or as human labelers what's easy for us or hard for us is different than what's easy or hard

中文：或许点赞会更好一些 或许应该再铺开一些。 最好将其设置为 方程式或许更好 深入讨论，我们根本做不到。 知道，我们也不知道，因为什么是…… 对你我而言，作为人类，这很容易。 标签标注者认为这对我们来说很容易，对他们来说却很难。 我们与容易或困难的事物不同。

### 2:18:16–2:18:43

EN：for the llm it cognition is different um and the token sequences are kind of like different hard for it and so some of the token sequences here that are trivial for me might be um very too much of a leap for the llm so right here this token would be way too hard but conversely many of the tokens that I'm creating here might be just trivial to

中文：对于LLM来说，认知是不同的。 而标记序列有点像 不同的是，它很难做到，所以有些…… 这里是一些无关紧要的标记序列 对我来说，这可能太……太多了 为了获得LLM学位，就在这里。 代币太难获取了，但是 相反，我拥有的许多代币 在这里创作可能微不足道

### 2:18:43–2:19:02

EN：the llm and we're just wasting tokens like why waste all these tokens when this is all trivial so if the only thing we care care about is the final answer and we're separating out the issue of the presentation to the human um then we don't actually really know how to annotate this example we don't know what solution to get to the llm because we are not the

中文：llm，我们只是在浪费代币。 为什么要浪费这些代币呢？ 这一切都是微不足道的，所以如果唯一的问题是 我们关心的，就是最终答案。 我们正在单独讨论这个问题。 向人类进行演示，嗯，然后我们 其实不太清楚该怎么做 请为这个例子添加注释，我们不知道是什么 获得法学硕士学位的办法是…… 不是

### 2:19:02–2:19:23

EN：llm and it's clear here in the case of like the math example but this is actually like a very pervasive issue like for our knowledge is not lm's knowledge like the llm actually has a ton of knowledge of PhD in math and physics chemistry and whatnot so in many ways it actually knows more than I do and I'm I'm potentially not utilizing that knowledge in its problem solving

中文：llm，这一点在这里很明显。 就像数学例子一样，但这是 实际上，这就像一个非常普遍的问题。 就我们所知，这并非lm的 像法学硕士这样的知识实际上具有 拥有数学博士学位的大量知识 物理、化学等等，在很多方面都是如此。 它实际上比我更了解很多方面 我可能没有充分利用 这种知识在解决问题中的作用

### 2:19:24–2:19:49

EN：but conversely I might be injecting a bunch of knowledge in my solutions that the LM doesn't know in its parameters and then those are like sudden leaps that are very confusing to the model and so our cognitions are different and I don't really know what to put here if all we care about is the reaching the final solution and doing it economically ideally and so long story short we are

中文：但反过来，我可能正在注射一种 我的解决方案中包含大量知识。 LM在其参数中并不知道 然后，那些就像是突然的飞跃。 这对模型来说非常令人困惑，而且 所以我们认知方式不同，而且我 不知道这里该写些什么 我们只关心达到目标 最终解决方案，并且经济高效 理想情况下，简而言之，我们是

### 2:19:49–2:20:14

EN：not in a good position to create these uh token sequences for the LM and they're useful by imitation to initialize the system but we really want the llm to discover the token sequences that work for it we need to find it needs to find for itself what token sequence reliably gets to the answer given the prompt and it needs to discover that in the process of reinforcement learning and of trial and

中文：目前的情况不利于创造这些 语言模型的标记序列 它们通过模仿而发挥作用 初始化系统，但我们真正想要 llm 用于发现令牌序列 我们需要找到它来为它工作。 需要自行找到哪个令牌 按照这个顺序就能可靠地得到答案 根据提示，它需要 发现在此过程中 强化学习和试验

### 2:20:14–2:20:39

EN：error so let's see how this example would work like in reinforcement learning okay so we're now back in the huging face inference playground and uh that just allows me to very easily call uh different kinds of models so as an example here on the top right I chose the Gemma 2 2 billion parameter model so two billion is very very small so this is a tiny model but it's okay so we're

中文：错误，让我们看看这个例子 就像加固一样。 学习 好了，我们现在又开始拥抱了。 面部识别游乐场，还有那个 这让我可以很方便地打电话…… 不同类型的模型，因此 例如，我在右上角选择 Gemma 2 20亿参数模型 20亿非常非常少，所以 虽然是个小模型，但没关系，所以我们……

### 2:20:39–2:21:02

EN：going to give it um the way that reinforcement learning will basically work is actually quite quite simple um we need to try many different kinds of solutions and we want to see which Solutions work well or not so we're basically going to take the prompt we're going to run the model and the model generates a solution and then we're going to inspect the solution and we know that the correct

中文：打算用这种方式…… 强化学习基本上 这项工作其实相当简单。 我们需要尝试多种不同的 解决方案，我们想看看哪些方案可行​​。 解决方案是否有效 所以我们基本上要采取 提示我们将要运行 模型，并且该模型生成解决方案 然后我们将检查…… 解决方案，我们知道正确的

### 2:21:02–2:21:23

EN：answer for this one is $3 and so indeed the model gets it correct it says it's $3 so this is correct so that's just one attempt at DIS solution so now we're going to delete this and we're going to rerun it again let's try a second attempt so the model solves it in a bit slightly different way right every single attempt will be a different generation because these models are

中文：答案是 3 美元，确实如此。 模型预测正确，它说是 3美元，所以这个数是正确的，所以这只是一个。 尝试使用DIS解决方案，所以现在我们是 我要删除这个，然后我们要…… 再运行一次，我们试试第二个。 尝试一下，模型很快就能解决这个问题。 略有不同的方式，每 单次尝试的结果会有所不同。 因为这些模型是一代产品。

### 2:21:23–2:21:46

EN：stochastic systems remember that at every single token here we have a probability distribution and we're sampling from that distribution so we end up kind kind of going down slightly different paths and so this is a second solution that also ends in the correct answer now we're going to delete that let's go a third time okay so again slightly different solution but also gets it correct now we can actually repeat this

中文：随机系统记住，在 这里每一个代币我们都有 概率分布，我们是 从该分布中抽样，因此我们 最后有点儿往下走。 不同的路径，所以这是第二个 最终结果也正确的解决方案 现在回答，我们要删除它。 我们去第三个 时间到了，所以又有点不一样了。 解决方案，但也得到了它 现在我们确实可以重复这个过程了。

### 2:21:46–2:22:06

EN：uh many times and so in practice you might actually sample thousand of independent Solutions or even like million solutions for just a single prompt um and some of them will be correct and some of them will not be very correct and basically what we want to do is we want to encourage the solutions that lead to correct answers so let's take a look at what that looks

中文：很多次，所以在实践中你 实际上可能会抽取数千个样本 独立解决方案，甚至类似 仅需一个解决方案，即可获得百万个解决方案 提示嗯，其中一些会是 正确，但其中一些不正确。 非常正确，这正是我们想要的。 我们这样做是为了鼓励…… 能够得出正确答案的解决方案 那么，让我们来看看它长什么样。

### 2:22:06–2:22:28

EN：like so if we come back over here here's kind of like a cartoon diagram of what this is looking like we have a prompt and then we tried many different solutions in parallel and some of the solutions um might go well so they get the right answer which is in green and some of the solutions might go poorly and may not reach the right answer which is red now

中文：就像这样，如果我们回到这里，这里是…… 有点像卡通图解，说明什么 看来我们有一个提示 然后我们尝试了很多不同的方法。 解决方案 并行和一些解决方案 可能会进展顺利，这样他们就能得到正确的结果。 答案以绿色显示，还有一些 解决方案可能效果不佳，也可能不会有效。 现在找到正确答案，答案是红色的。

### 2:22:28–2:22:54

EN：this problem here unfortunately is not the best example because it's a trivial prompt and as we saw uh even like a two billion parameter model always gets it right so it's not the best example in that sense but let's just exercise some imagination here and let's just suppose that the um green ones are good and the red ones are bad okay so we generated 15 Solutions only four of them got the right answer

中文：很遗憾，这里的问题并非如此。 这是最好的例子，因为它很简单。 迅速，正如我们所见，甚至像两个 十亿参数模型总是能成功 对，所以这并不是最好的例子。 那种感觉，但我们不妨练习一下。 这里只是发挥想象力，我们不妨假设一下 绿色的那些很好，而且 红色的是 好的，我们生成了 15 个解决方案。 只有四个人答对了。

### 2:22:54–2:23:18

EN：and so now what we want to do is basically we want to encourage the kinds of solutions that lead to right answers so whatever token sequences happened in these red Solutions obviously something went wrong along the way somewhere and uh this was not a good path to take through the solution and whatever token sequences there were in these Green Solutions well things went uh pretty well in this situation and so we want to

中文：所以现在我们想做的是…… 我们基本上是想鼓励这类行为 能够得出正确答案的解决方案 所以无论发生了什么标记序列 这些红色溶液显然是某种东西 过程中某个环节出了问题， 呃，这不是一条好路。 通过解决方案和任何令牌 这些绿色序列中存在 解决方案嘛，事情进展得相当顺利。 在这种情况下，我们想要

### 2:23:18–2:23:40

EN：do more things like it in prompts like this and the way we encourage this kind of a behavior in the future is we basically train on these sequences um but these training sequencies now are not coming from expert human annotators there's no human who decided that this is the correct solution this solution came from the model itself so the model is practicing here it's tried out a few

中文：在类似提示中多做一些类似的事情，例如 以及我们鼓励这种行为的方式 未来行为的预测是我们 基本上就是用这些序列进行训练。 但现在的这些训练序列是 并非来自专家人工标注员 没有人决定这一点。 这个解决方案是正确的吗？ 源自模型本身，因此该模型 正在这里练习，它已经尝试了一些

### 2:23:40–2:23:58

EN：Solutions four of them seem to have worked and now the model will kind of like train on them and this corresponds to a student basically looking at their Solutions and being like okay well this one worked really well so this is this is how I should be solving these kinds of problems and uh here in this example there are many different ways to actually like really tweak the

中文：其中四种解决方案似乎都 成功了，现在这个模型会有点…… 就像在它们上面训练一样，这与之对应 对一个学生来说，基本上是在看他们的 解决方案就像，好吧，这样 其中一个效果非常好，所以这是这个 这就是我应该解决这类问题的方式。 问题，呃，在这个例子中 有很多不同的方法 实际上，我真的想好好调整一下

### 2:23:58–2:24:17

EN：methodology a little bit here but just to give the core idea across maybe it's simplest to just think about take the taking the single best solution out of these four uh like say this one that's why it was yellow uh so this is the the solution that not only led to the right answer but may maybe had some other nice properties maybe it was the shortest one

中文：方法论方面这里稍微有点涉及，但仅此而已。 为了传达核心思想，或许是这样。 最简单的办法就是想想…… 从中找出最佳解决方案 这四个，呃，比如说这个，就是这个 为什么它是黄色的？呃，所以这就是…… 不仅找到了正确的解决方案 答案或许还有其他不错的选择。 属性或许它是最短的

### 2:24:17–2:24:38

EN：or it looked nicest in some ways or uh there's other criteria you could think of as an example but we're going to decide that this the top solution we're going to train on it and then uh the model will be slightly more likely once you do the parameter update to take this path in this kind of a setting in the future but you have to remember that

中文：或者在某些方面看起来最漂亮，或者呃 还有其他一些标准可以考虑。 举个例子，但我们接下来要…… 决定这是我们目前为止的最佳解决方案。 准备进行相关训练，然后…… 一旦模型出现，出现的可能性会略微增加。 你需要进行参数更新才能实现这一点。 在这种环境下的路径 未来，但你必须记住这一点。

### 2:24:38–2:25:02

EN：we're going to run many different diverse prompts across lots of math problems and physics problems and whatever wherever there might be so tens of thousands of prompts maybe have in mind there's thousands of solutions prompt and so this is all happening kind of like at the same time and as we're iterating this process the model is discovering for itself what kinds of token sequences lead it to correct

中文：我们将运行许多不同的 数学中各种各样的提示 问题和物理问题 无论在哪里，可能有几十个 成千上万个提示中可能包含 请注意，解决方案有成千上万种。 提示，所以这一切都在发生。 同时，就像我们一样 通过迭代这个过程，模型是 它自行探索各种 标记序列使其正确

### 2:25:02–2:25:28

EN：answers it's not coming from a human annotator the the model is kind of like playing in this playground and it knows what it's trying to get to and it's discovering sequences that work for it uh these are sequences that don't make any mental leaps uh they they seem to work reliably and statistically and uh fully utilize the knowledge of the model as it has it and so uh this is the

中文：答案并非来自人类 标注器，模型有点像 在这个游乐场玩耍，它知道 它试图达到的目的，以及它的…… 发现适合它的序列 呃，这些序列不会产生 任何思维跳跃，呃，他们似乎 工作可靠且具有统计学意义，呃 充分利用模型知识 因为它就是这样，所以，呃，这就是……

### 2:25:28–2:25:48

EN：process of reinforcement learning it's basically a guess and check we're going to guess many different types of solutions we're going to check them and we're going to do more of what worked in the future and that is uh reinforcement learning so in the context of what came before we see now that the sft model the supervised fine tuning model it's still helpful because it still kind of like initializes the

中文：强化过程 学习它基本上是一种猜测， 检查一下，我们要猜很多。 我们正在探索不同类型的解决方案 我们会检查它们，而且我们还会做更多工作。 未来哪些做法行之有效，那就是 呃，强化学习，所以在 我们现在所看到的，是之前发生的事件的背景。 sft模型监督精细化 调整模型仍然有用，因为 它仍然有点像初始化

### 2:25:49–2:26:07

EN：model a little bit into to the vicinity of the correct Solutions so it's kind of like a initialization of um of the model in the sense that it kind of gets the model to you know take Solutions like write out Solutions and maybe it has an understanding of setting up a system of equations or maybe it kind of like talks through a solution so it gets you into

中文：模型稍微靠近附近 正确的解决方案有很多，所以这有点像 就像对模型进行初始化一样 从某种意义上说，它得到了 你知道，这样的模型可以采取解决方案，例如 写出解决方案，也许它有…… 了解如何建立系统 方程式，或者也许有点像谈话 通过一个解决方案，让你进入

### 2:26:08–2:26:27

EN：the vicinity of correct Solutions but reinforcement learning is where everything gets dialed in we really discover the solutions that work for the model get the right answers we encourage them and then the model just kind of like gets better over time time okay so that is the high Lev process for how we train large language models in short we train them kind of very similar to how

中文：正确解的附近 强化学习是其中 一切都调整到位了，我们真的 找到适合的解决方案 模型能够得出我们鼓励的正确答案 它们，然后模型就有点像这样了。 就像随着时间的推移情况会好转一样，好的。 这就是我们高阶流程的运作方式 简而言之，我们训练大型语言模型 训练他们的方式与训练方法非常相似

### 2:26:27–2:26:49

EN：we train children and basically the only difference is that children go through chapters of books and they do all these different types of training exercises um kind of within the chapter of each book but instead when we train AIS it's almost like we kind of do it stage by stage depending on the type of that stage so first what we do is we do pre-training which as we saw is

中文：我们训练孩子，而且基本上是唯一 区别在于孩子们要经历 书中的章节，他们做了所有这些 不同类型的训练练习 有点像每本书的章节里的内容 但当我们训练AIS时，情况却是…… 几乎就像我们按阶段来做一样。 阶段取决于该类型的 阶段，所以首先我们要做的就是 预训练，正如我们所看到的，是

### 2:26:49–2:27:11

EN：equivalent to uh basically reading all the expository material so we look at all the textbooks at the same time and we read all the exposition and we try to build a knowledge base the second thing then is we go into the sft stage which is really looking at all the fixed uh sort of like solutions from Human Experts of all the different kinds of worked Solutions across all the

中文：相当于基本上读完所有内容 所以我们来看一下说明性材料。 同时阅读所有教科书 我们阅读了所有说明文字，并尝试…… 第二件事是建立知识库。 然后我们就进入软件开发阶段， 实际上是在审视所有固定的呃 有点像来自人类的解决方案 各类专家 适用于所有解决方案

### 2:27:11–2:27:30

EN：textbooks and we just kind of get an sft model which is able to imitate the experts but does so kind of blindly it just kind of like does its best guess uh kind of just like trying to mimic statistically the expert behavior and so that's what you get when you look at all the work Solutions and then finally in the last stage we do all the practice

中文：教科书，我们基本上就得到了一个sft 能够模仿的模型 专家们这样做，但却有些盲目。 就好像它尽力猜测一样 嗯，有点像是在模仿 从统计学角度来看，专家的行为等等 这就是你纵观一切所得到的。 工作解决方案，最后在 最后阶段我们进行所有的练习。

### 2:27:30–2:27:52

EN：problems in the RL stage across all the textbooks we only do the practice problems and that's how we get the RL model so on a high level the way we train llms is very much equivalent uh to the process that we train uh that we use for training of children the next point I would like to make is that actually these first two stat ages pre-training and surprise fine-tuning they've been

中文：强化学习阶段所有方面的问题 我们只做教科书上的练习题。 问题就出在这里，这就是我们获得强化学习的方式。 因此，从宏观层面来说，我们的模型就是我们这样做的方式。 训练 llms 与 uh 非常相似 我们训练的流程，我们使用的流程。 关于儿童训练的下一个要点 我想做的就是实际上 前两个统计数据适用于训练前 以及他们一直在进行的出人意料的微调

## 18. DeepSeek-R1（2:27:47–2:42:07）

### 2:27:52–2:28:13

EN：around for years and they are very standard and everyone does them all the different llm providers it is this last stage the RL training that is a lot more early in its process of development and is not standard yet in the field and so um this stage is a lot more kind of early and nent and the reason for that is because I actually skipped over a ton

中文：它们存在多年，而且非常 这些都是标准操作，每个人都会做。 不同的LLM提供商，这是最后一个。 启动更复杂的强化学习训练。 在其发展过程的早期阶段和 目前这还不是该领域的标准做法，因此 嗯，这个阶段更像是…… 早晚以及原因 因为我实际上跳过了很多内容。

### 2:28:13–2:28:30

EN：of little details here in this process the high level idea is very simple it's trial and there learning but there's a ton of details and little math mathematical kind of like nuances to exactly how you pick the solutions that are the best and how much you train on them and what is the prompt distribution and how to set up the training run such that this actually works so there's a

中文：这个过程中的一些小细节也很重要。 其核心思想非常简单： 尝试和学习，但还有 细节很多，数学成分很少 数学上的某种细微差别 你究竟是如何选择解决方案的？ 最好的训练量取决于你的训练水平。 它们以及什么是快速分配 以及如何设置训练运行 这确实有效，所以……

### 2:28:30–2:28:55

EN：lot of little details and knobs to the core idea that is very very simple and so getting the details right here uh is not trivial and so a lot of companies like for example open and other LM providers have experimented internally with reinforcement learning fine tuning for llms for a while but they've not talked about it publicly um it's all kind of done inside the company and so that's why the paper from

中文：有很多小细节和旋钮 核心思想非常非常简单， 所以，把细节弄对是…… 这并非微不足道，因此很多公司 例如开放的、其他的LM 供应商已在内部进行过试验 通过强化学习进行微调 他们之前一直想申请LLMS，但他们没有。 公开谈论过这件事 嗯，这一切都是在内部完成的。 公司，所以才有了这份文件。

### 2:28:55–2:29:18

EN：Deep seek that came out very very recently was such a big deal because this is a paper from this company called DC Kai in China and this paper really talked very publicly about reinforcement learning fine training for large language models and how incredibly important it is for large language models and how it brings out a lot of reasoning capabilities in the models we'll go into this in a second so this

中文：深入的寻找，结果非常非常 最近这件事之所以如此重要，是因为 这是这家公司出具的一份文件，名为 DC Kai在中国，而这篇论文确实 公开谈论强化 为大型企业学习精细训练 语言模型及其令人难以置信的之处 对于大型语言来说，这一点很重要 模型以及它如何展现出很多东西 模型中的推理能力 我们稍后会详细讨论这个问题。

### 2:29:18–2:29:39

EN：paper reinvigorated the public interest of using RL for llms and gave a lot of the um sort of n-r details that are needed to reproduce their results and actually get the stage to work for large langage models so let me take you briefly through this uh deep seek R1 paper and what happens when you actually correctly apply RL to language models and what that looks like and what that

中文：该报重新激发了公众的兴趣。 使用强化学习进行语言学习管理系统（LLMS）并给出了很多建议 嗯，那种n-r细节是 需要重现他们的结果 真正让舞台为大型活动服务 语言模型，让我带你了解一下。 简要地通过这个深度搜索 R1 纸张以及当你实际使用时会发生什么 将强化学习正确应用于语言模型 以及那看起来是什么样子，以及那是什么

### 2:29:39–2:29:58

EN：gives you so the first thing I'll scroll to is this uh kind of figure two here where we are looking at the Improvement in how the models are solving mathematical problems so this is the accuracy of solving mathematical problems on the a accuracy and then we can go to the web page and we can see the kinds of problems that are actually in these um these the kinds of math

中文：给你，所以我首先要滚动查看 这是图二吗？ 我们正在关注改进之处。 模型如何解决问题 这就是数学问题 数学求解的准确性 精度方面存在问题，然后我们 可以访问该网页，然后我们就可以看到 实际存在的问题类型 在这些数学类型中

### 2:29:58–2:30:17

EN：problems that are being measured here so these are simple math problems you can um pause the video if you like but these are the kinds of problems that basically the models are being asked to solve and you can see that in the beginning they're not doing very well but then as you update the model with this many thousands of steps their accuracy kind of continues to climb so the models are

中文：这里正在衡量的问题 这些都是简单的数学题，你可以解答。 嗯，如果你愿意的话可以暂停视频，但是这些 基本上就是这类问题。 这些模型被要求解决以下问题： 你可以看到，一开始就是这样。 他们做得不太好，但是后来…… 您使用这么多更新了模型 数千步，它们的精确度 持续攀升，因此模型是

### 2:30:17–2:30:40

EN：improving and they're solving these problems with a higher accuracy as you do this trial and error on a large data set of these kinds of problems and the models are discovering how to solve math problems but even more incredible than the quantitative kind of results of solving these problems with a higher accuracy is the qualitative means by which the model achieves these results so when we scroll down uh one of

中文：情况正在好转，他们正在解决这些问题。 精度更高的问题 当你进行这种反复试验时 这类大型数据集 问题和模型正在发现 如何解决数学问题，但更重要的是 比定量分析更令人难以置信 用以下方法解决这些问题的结果 更高的准确度是定性手段 该模型通过以下方式实现这些目标 结果，当我们向下滚动时，其中一个

### 2:30:40–2:31:05

EN：the figures here that is kind of interesting is that later on in the optimization the model seems to be uh using average length per response uh goes up up so the model seems to be using more tokens to get its higher accuracy results so it's learning to create very very long Solutions why are these Solutions very long we can look at them qualitatively here so basically what they discover is that the model

中文：这里的数据有点…… 有趣的是，后来…… 优化模型似乎是…… 使用平均响应长度 向上移动，所以模型看起来是 使用更多代币来获得更高的收益 准确率结果，所以它正在学习 为什么会创建非常非常长的解决方案？ 这些解决方案需要很长时间才能让我们开始研究。 从定性角度来看，基本上就是这样。 他们发现的模型

### 2:31:05–2:31:25

EN：solution get very very long partially because so here's a question and here's kind of the answer from the model what the model learns to do um and this is an immerging property of new optimization it just discovers that this is good for problem solving is it starts to do stuff like this wait wait wait that's Nota moment I can flag here let's reevaluate this step by step to identify the

中文：解决方案变得非常非常长，部分 因为这里有个问题，还有…… 模型给出的答案是什么？ 该模型学会了做……嗯，这是一个…… 新优化的涌现特性 它只是发现这对……有好处 解决问题就是开始行动。 像这样，等等，等等，那是 Nota 我现在可以在这里标记一下，让我们重新评估一下。 通过以下步骤来识别

### 2:31:25–2:31:48

EN：correct sum can be so what is the model doing here right the model is basically re-evaluating steps it has learned that it works better for accuracy to try out lots of ideas try something from different perspectives retrace reframe backtrack is doing a lot of the things that you and I are doing in the process of problem solving for mathematical questions but it's rediscovering what happens in your head not what you put

中文：正确的总和可以是多少，那么模型是什么？ 这里正确地使用模型基本上是 重新评估已学到的步骤 为了提高准确性，可以尝试一下。 有很多想法，可以尝试一下。 不同的视角，回顾，重新定义 回溯功能做了很多事情 在这个过程中，你我正在做的事情 数学问题解决 问题，但它正在重新发现什么 事情的发生取决于你的思想，而不是你所表达的。

### 2:31:48–2:32:08

EN：down on the solution and there is no human who can hardcode this stuff in the ideal assistant response this is only something that can be discovered in the process of reinforcement learning because you wouldn't know what to put here this just turns out to work for the model and it improves its accuracy in problem solving so the model learns what we call these chains of thought in your

中文：解决方案很糟糕，没有办法。 能把这些东西硬编码进去的人。 理想的助手回应仅 可以在以下方面发现的东西 强化学习过程 因为你不知道该放什么。 结果证明，这种方法对……有效。 该模型提高了其准确性 解决问题，以便模型能够学习什么 我们称这些为你的思维链。

### 2:32:08–2:32:33

EN：head and it's an emergent property of the optim of the optimization and that's what's bloating up the response length but that's also what's increasing the accuracy of the problem problem solving so what's incredible here is basically the model is discovering ways to think it's learning what I like to call cognitive strategies of how you manipulate a problem and how you approach it from different perspectives how you pull in some analogies or do

中文：头部，它是涌现属性 优化中的优化，那就是 是什么导致响应长度过长 但这同时也是导致这种情况加剧的原因。 问题解决的准确性 所以，这里最不可思议的是…… 该模型正在探索思考方式 这是学习我喜欢称之为 你如何运用认知策略 操纵问题以及你如何 从不同角度看待这个问题 你是如何引入一些类比的，或者怎么做？

### 2:32:33–2:32:54

EN：different kinds of things like that and how you kind of uh try out many different things over time uh check a result from different perspectives and how you kind of uh solve problems but here it's kind of discovered by the RL so extremely incredible to see this emerge in the optimization without having to hardcode it anywhere the only thing we've given it are the correct answers and this comes out from trying

中文：诸如此类的各种事情 你如何尝试很多 随着时间的推移，不同的事情会发生，嗯，检查一下 从不同角度得出的结果 你是如何解决问题的？ 这里算是RL发现的吧。 看到这一幕真是太不可思议了 在优化过程中出现，而无需 必须在任何地方硬编码，这是唯一的办法。 我们给它的东西是正确的 答案来自尝试

### 2:32:54–2:33:15

EN：to just solve them correctly which is incredible um now let's go back to actually the problem that we've been working with and let's take a look at what it would look like uh for uh for this kind of a model what we call reasoning or thinking model to solve that problem okay so recall that this is the problem we've been working with and when I pasted it into

中文：只需正确解答这些问题即可。 极好的 嗯，现在让我们回到正题。 我们一直在努力解决的问题 我们来看看它会是什么样子。 比如，呃，对于这种模型 我们称之为推理或思维模型 为了解决这个问题，好的，所以回忆一下 这就是我们一直以来面临的问题。 正在处理并粘贴到

### 2:33:15–2:33:37

EN：chat GPT 40 I'm getting this kind of a response let's take a look at what happens when you give this same query to what's called a reasoning or a thinking model this is a model that was trained with reinforcement learning so this model described in this paper DC car1 is available on chat. dec.com uh so this is kind of like the company uh that developed is hosting it you have to make

中文：聊天 GPT 40 我遇到了这种问题 回应：我们来看看…… 当你向以下对象发送相同的查询时，就会发生这种情况： 所谓推理或思考 这是一个经过训练的模型 通过强化学习，所以这 本文所述模型为直流车1 在线聊天。 dec.com 嗯，所以这是 有点像那家公司…… 开发完成并托管，你必须这样做。

### 2:33:37–2:33:58

EN：sure that the Deep think button is turned on to get the R1 model as it's called we can paste it here and run it and so let's take a look at what happens now and what is the output of the model okay so here's it says so this is previously what we get using basically what's an sft approach a supervised funing approach this is like mimicking an expert solution this is

中文：确定“深度思考”按钮是 已开启以获取 R1 型号，因为它是 我们可以把它粘贴到这里并运行 那么，让我们来看看它是什么。 现在发生了什么？输出结果是什么？ 模型好的，它上面写着： 这是我们以前使用所得到的结果 基本上，什么是软件框架方法？ 监督式娱乐方法就像这样 这是模仿专家解决方案的做法。

### 2:33:58–2:34:23

EN：what we get from the RL model okay let me try to figure this out so Emily buys three apples and two oranges each orange cost $2 total is 13 I need to find out blah blah blah so here you you um as you're reading this you can't escape thinking that this model is thinking um is definitely pursuing the solution solution it deres that it must cost $3 and then it says wait a second

中文：我们从强化学习模型中得到什么？好的，让我们 我试着弄明白这件事，这样艾米丽就会买了。 三个苹果和两个橙子，每个橙子 总共花费 2 美元，总共是 13 美元，我需要弄清楚。 巴拉巴拉巴拉，所以你在这里，嗯，作为 你正在读这篇文章，你无法逃脱 认为这个模型是 思考嗯，这绝对是在追求 解决方案必须 花费 3 美元，然后提示稍等片刻

### 2:34:23–2:34:44

EN：let me check my math again to be sure and then it tries it from a slightly different perspective and then it says yep all that checks out I think that's the answer I don't see any mistakes let me see if there's another way to approach the problem maybe setting up an equation let's let the cost of one apple be $8 then blah blah blah yep same answer so definitely each apple is $3

中文：让我再检查一遍我的计算，确保万无一失。 然后它尝试从一个略微的角度进行。 不同的视角，然后它说 是的，所有这些都符合要求，我想就是这样。 我没看出答案有什么错误。 我看看有没有其他办法 解决这个问题的方法可能是建立一个 假设一个苹果的价格为： 如果是 8 美元，那就等等等等，没错，一样。 答案是肯定的，每个苹果3美元。

### 2:34:44–2:35:05

EN：all right confident that that's correct and then what it does once it sort of um did the thinking process is it writes up the nice solution for the human and so this is now considering so this is more about the correctness aspect and this is more about the presentation aspect where it kind of like writes it out nicely and uh boxes in the correct answer at the

中文：好的，我确信这是正确的。 然后它接下来会做什么呢？嗯…… 思考过程是写出来的吗？ 对人类来说，这是一个不错的解决方案，因此 目前正在考虑这一点，所以这更多 关于正确性方面，这是 更多关于演示方面的信息 它就像是把它写得很清楚一样。 呃，正确答案中的方框

### 2:35:05–2:35:29

EN：bottom and so what's incredible about this is we get this like thinking process of the model and this is what's coming from the reinforcement learning process this is what's bloating up the length of the token sequences they're doing thinking and they're trying different ways this is what's giving you higher accuracy in problem solving and this is where we are seeing these aha moments and these different strategies and these um ideas for how

中文：底部，那么，最不可思议的是什么？ 这就是我们理解的那种感觉。 模型的运行过程，这就是…… 来自强化学习 这个过程就是导致程序膨胀的原因。 它们是标记序列的长度 他们正在思考，并且正在尝试 这就是它带给你的不同方式。 问题解决率更高 解决之道就在这里，我们看到了这一点。 这些顿悟时刻和这些不同的 策略以及这些想法，关于如何

### 2:35:29–2:35:52

EN：you can make sure that you're getting the correct answer the last point I wanted to make is some people are a little bit nervous about putting you know very sensitive data into chat.com because this is a Chinese company so people don't um people are a little bit careful and Cy with that a little bit um deep seek R1 is a model that was released by this company so this is an open source model

中文：你可以确保你得到 正确 回答我最后一点想说的话。 有些人会有点紧张 关于放置你知道非常敏感的东西 数据会传输到 chat.com，因为这是一个 中国公司，所以人们不…… 人们都比较谨慎，还有赛伊 稍微深入一点寻找R1 这是由该机构发布的一款模型。 所以这是一个开源模型。

### 2:35:52–2:36:14

EN：or open weights model it is available for anyone to download and use you will not be able to like run it in its full um sort of the full model in full Precision you won't run that on a MacBook but uh or like a local device because this is a fairly large model but many companies are hosting the full largest model one of those companies that I like to use is called

中文：或者，它也可以采用公开重量级模式。 任何人都可以下载和使用 无法完整运行它。 嗯，算是完整的模型吧。 精确度方面，你不会在……上运行它 MacBook，或者像本地设备一样 因为这是一个相当大的模型，但是 许多公司都在举办完整的 这些公司中最大的型号之一 我喜欢用的那个叫做

### 2:36:14–2:36:33

EN：together. so when you go to together. you sign up and you go to playgrounds you can can select here in the chat deep seek R1 and there's many different kinds of other models that you can select here these are all state-of-the-art models so this is kind of similar to the hugging face inference playground that we've been playing with so far but together. a will usually host all the

中文：一起。所以当你们一起去的时候。 你注册后就可以去游乐场了。 您可以在这里选择聊天深度 寻找 R1，有很多不同的种类 您可以在这里选择其他型号。 这些都是最先进的型号，所以 这有点像拥抱 我们已经搭建了一个面部识别实验场。 目前为止我们一直一起玩。一个 通常会托管所有

### 2:36:33–2:36:55

EN：state-of-the-art models so select DT car1 um you can try to ignore a lot of these I think the default settings will often be okay and we can put in this and because the model was released by Deep seek what you're getting here should be basically equivalent to what you're getting here now because of the randomness in the sampling we're going to get something slightly different uh but in principle this should be uh

中文：选择最先进的模型 DT car1 嗯，你可以试着忽略很多 我认为这些是默认设置。 通常没问题，我们可以把这个放进去。 因为该模型是由Deep发布的。 你应该明白你在这里能得到什么。 基本上相当于你 现在来到这里是因为 我们正在进行随机抽样。 想要一些稍微不同的东西…… 但原则上这应该是……

### 2:36:55–2:37:15

EN：identical in terms of the power of the model and you should be able to see the same things quantitatively and qualitatively uh but uh this model is coming from kind of a an American company so that's deep seek and that's the what's called a reasoning model now when I go back to chat uh let me go to chat here okay so the models that you're going to see in the drop

中文：就功率而言，两者相同 模型，你应该能够看到 数量上相同， 从定性角度来看，但是这个模型是 有点像美国人 公司，所以这是深入的探寻，就是这样。 所谓推理 现在我回去聊天的时候，模型就……呃，让 我去这里聊天，好的，所以是这些模型。 你会在下降过程中看到这一点。

### 2:37:15–2:37:40

EN：down here some of them like 01 03 mini O3 mini High Etc they are talking about uses Advanced reasoning now what this is referring to uses Advanced reasoning is it's referring to the fact that it was trained by reinforcement learning with techniques very similar to those of deep C car1 per public statements of opening ey employees uh so these are thinking models trained with RL and these models

中文：下面有些像01 03 mini 他们谈论的是 O3 mini High 等等 现在，我们来谈谈高级推理。 指的是运用高级推理 它指的是这样一个事实： 通过强化学习进行训练 技术与深层技术非常相似。 C car1 根据公开声明开幕 嘿，员工们，呃，所以这些都在思考 使用强化学习训练的模型以及这些模型

### 2:37:40–2:37:58

EN：like GPT 4 or GPT 4 40 mini that you're getting in the free tier you should think of them as mostly sft models supervised fine tuning models they don't actually do this like thinking as as you see in the RL models and even though there's a little bit of reinforcement learning involved with these models and I'll go that into that in a second these are mostly sft models I think you should

中文：比如 GPT 4 或 GPT 4 40 mini，你 你应该先加入免费层级 可以把它们看作是大多数软件模型。 他们不进行监督式微调模型 实际上，就像你思考时那样去做。 在强化学习模型中可以看到，即使 有一些加固措施 这些模型所涉及的学习以及 我马上就详细说说这些。 我认为它们大多是软件模型，你应该

### 2:37:58–2:38:20

EN：think about it that way so in the same way as what we saw here we can pick one of the thinking models like say 03 mini high and these models by the way might not be available to you unless you pay a Chachi PT subscription of either $20 per month or $200 per month for some of the top models so we can pick a thinking model and run now what's going to happen

中文：那样想，同样地。 根据我们在这里看到的，我们可以选择一种方式。 例如 03 型迷你思维模型 顺便说一句，这些型号可能很高。 除非你付费，否则你将无法使用。 Chachi PT订阅费为20美元 每月或每月 200 美元，适用于某些情况 顶级模特，这样我们就可以挑选一个有想法的人。 现在建模并运行，看看会发生什么

### 2:38:20–2:38:42

EN：here is it's going to say reasoning and it's going to start to do stuff like this and um what we're seeing here is not exactly the stuff we're seeing here so even though under the hood the model produces these kinds of uh kind of chains of thought opening ey chooses to not show the exact chains of thought in the web interface it shows little summaries of that of those chains of

中文：这里会提到理由和 它将开始做一些类似的事情，比如 这个，还有我们在这里看到的是…… 跟我们在这里看到的并不完全一样。 所以即使在模型内部 产生这类…… 思维链的开启，他们选择 不显示确切的思路链 网页界面显示的内容很少 对这些链条的总结

### 2:38:42–2:39:02

EN：thought and open kind of does this I think partly because uh they are worried about what's called the distillation risk that is that someone could come in and actually try to imitate those reasoning traces and recover a lot of the reasoning performance by just imitating the reasoning uh chains of thought and so they kind of hide them and they only show little summaries of them so you're not getting exactly what

中文：思考和开放的态度，我就是这样做的。 部分原因是他们很担心 关于所谓的蒸馏 风险在于有人可能会进来。 并且尝试模仿那些 推理痕迹并恢复大量 仅通过推理性能 模仿推理链 所以他们会想办法把它们藏起来。 它们只显示一些简短的摘要 所以你并没有得到确切的信息。

### 2:39:02–2:39:22

EN：you would get in deep seek as with respect to the reasoning itself and then they write up the solution so these are kind of like equivalent even though we're not seeing the full under the hood details now in terms of the performance uh these models and deep seek models are currently rly on par I would say it's kind of hard to tell because of the evaluations but if

中文：你会像……一样深入探索。 尊重推理本身，然后 他们写下了 解决方案，所以这些有点像…… 即使我们没有看到，其效果也是相同的。 完整的内部细节现已公布 就这些模型的性能而言 而深度搜索模型目前确实 我觉得很难说两者水平相当。 因为评估结果而告知，但如果

### 2:39:22–2:39:46

EN：you're paying $200 per month to open AI some of these models I believe are currently they basically still look better uh but deep seek R1 for now is still a very solid choice for a thinking model that would be available to you um sort of um either on this website or any other website because the model is open weights you can just download it so that's thinking models so what is the

中文：你每月要支付 200 美元才能使用 OpenAI 我认为其中一些模型是 目前它们基本上看起来仍然如此 更好的是，但目前深度搜索 R1 是 对于深思熟虑的人来说，这仍然是一个非常可靠的选择。 您可以选择的型号 某种程度上，要么在这个网站上，要么在任何其他地方。 其他网站，因为该模型是开放的 你可以直接下载重量数据。 这就是思维模型，那么什么是……

### 2:39:46–2:40:12

EN：summary so far well we've talked about reinforcement learning and the fact that thinking emerges in the process of the optimization on when we basically run RL on many math uh and kind of code problems that have verifiable Solutions so there's like an answer three Etc now these thinking models you can access in for example deep seek or any inference provider like together. a and choosing deep seek over there these

中文：总结一下，到目前为止，我们已经讨论了…… 强化学习以及以下事实 思维是在以下过程中产生的： 优化何时运行强化学习 在许多数学和各种代码中 有可验证解决方案的问题 所以答案是三。 等等，现在你可以使用这些思维模型 例如，在深度搜索或任何其他方式中进行访问 推理提供者喜欢在一起。和 选择深度搜索在那里这些

### 2:40:12–2:40:35

EN：thinking models are also available uh in chpt under any of the 01 or O3 models but these GPT 4 R models Etc they're not thinking models you should think of them as mostly sft models now if you are um if you have a prompt that requires Advanced reasoning and so on you should probably use some of the thinking models or at least try them out but empirically for a lot of my use when

中文：思维模型也可用 在任何 01 或 O3 章节下 但这些 GPT 4 R 模型等等 他们不是你应该考虑的模型 现在可以把它们看作是大多数软件模型。 如果你是嗯，如果你有一个提示， 需要高级推理能力等等 你或许应该使用一些 思考模型，或者至少尝试一下。 但就我的经验而言，当……

### 2:40:35–2:40:53

EN：you're asking a simpler question there's like a knowledge based question or something like that this might be Overkill like there's no need to think 30 seconds about some factual question so for that I will uh sometimes default to just GPT 40 so empirically about 80 90% of my use is just gp4 and when I come across a very difficult problem like in math and code Etc I will

中文：你问的是一个更简单的问题。 例如知识问答题 类似这样的事情或许会发生。 反应过度，好像根本不需要思考一样。 30秒回答一些事实性问题 所以为此，我有时会默认使用默认设置。 仅 GPT 40，根据经验约为 80 我90%的使用情况都只是GP4。 当我遇到一个非常困难的问题时 像数学和编程等方面的问题，我会

### 2:40:53–2:41:05

EN：reach for the thinking models but then I have to wait a bit longer because they're thinking um so you can access these on chat on deep seek also I wanted to point out that um AI studio.

中文：我试图运用思维模型，但是后来 还得再等一段时间，因为 他们想的是，这样你就可以访问了。 这些在深度探索聊天中也让我很感兴趣。 指出，嗯，人工智能工作室。

### 2:41:05–2:41:29

EN：go.com even though it looks really busy really ugly because Google's just unable to do this kind of stuff well it's like what is happening but if you choose model and you choose here Gemini 2.0 flash thinking experimental 01 21 if you choose that one that's also a a kind of early experiment experimental of a thinking model by Google so we can go here and we can give it the same problem

中文：go.com 虽然看起来很繁忙。 真是太糟糕了，因为谷歌根本做不到。 要做好这类事情，就像 发生了什么？但如果你选择 您在这里选择的是 Gemini 2.0 型号。 闪思实验 01 21 如果你 选择那种也是某种…… 早期实验的实验 谷歌的思维模型，所以我们可以去 在这里，我们可以提出同样的问题。

### 2:41:29–2:41:51

EN：and click run and this is also a thinking problem a thinking model that will also do something similar and comes out with the right answer here so basically Gemini also offers a thinking model anthropic currently does not offer a thinking model but basically this is kind of like the frontier development of these llms I think RL is kind of like this new exciting stage but getting the details

中文：点击运行，这也是 思考问题，一种思考模型 还会做某事 类似，并且得出了正确的结果。 答案就在这里，所以基本上也是双子座。 提供了一种人类学的思维模型 目前没有提供思考方式 模型，但基本上这有点像 这些LLMS的前沿发展 我觉得RL有点像这个新事物 激动人心的阶段，但细节仍需了解。

### 2:41:51–2:42:17

EN：right is difficult and that's why all these models and thinking models are currently experimental as of 2025 very early 2025 um but this is kind of like the frontier development of pushing the performance on these very difficult problems using reasoning that is emerging in these optimizations one more connection that I wanted to bring up is that the discovery that reinforcement learning is extremely powerful way of learning is not new to the field of AI

中文：正确的事情很难做，这就是为什么所有 这些模型和思维模型是 目前处于实验阶段，截至2025年非常 2025年初，嗯，但这有点像 推动前沿发展的 在这些非常困难的比赛中表现出色 运用推理解决问题 在这些优化中又出现了一个新的优化方案。 我想提出的联系是 发现强化作用 学习是一种极其强大的方式 学习对于人工智能领域来说并不新鲜。

## 19. AlphaGo（2:42:07–2:48:26）

### 2:42:17–2:42:43

EN：and one place what we've already seen this demonstrated is in the game of Go and famously Deep Mind developed the system alphago and you can watch a movie about it um where the system is learning to play the game of go against top human players and um when we go to the paper underlying alphago so in this paper when we scroll down we actually find a really

中文：以及我们已经看到的地方 这在围棋游戏中得到了体现。 其中最著名的当属Deep Mind开发的 使用 Alphago 系统，您可以观看电影。 关于它，嗯，系统正在学习的地方 与顶尖人类棋手对弈围棋 球员们，还有，嗯，当我们去看报纸的时候 本文中提到的底层AlphaGo 我们滚动 往下看，我们实际上发现了一个非常

### 2:42:43–2:43:05

EN：interesting plot um that I think uh is kind of familiar uh to us and we're kind of like we discovering in the more open domain of arbitrary problem solving instead of on the closed specific domain of the game of Go but basically what they saw and we're going to see this in llms as well as this becomes more mature is this is the ELO rating of playing game of Go

中文：有趣的 情节，嗯，我觉得这有点像…… 对我们来说很熟悉，我们有点像 我们在更开放的领域中发现了这一点 随意解决问题，而不是 在封闭的特定域上 围棋游戏，但基本上他们看到的是…… 我们将在LLMS中看到这一点。 随着这项技术日趋成熟，情况就是这样。 ELO等级分是围棋比赛的等级分。

### 2:43:05–2:43:28

EN：and this is leas dull an extremely strong human player and here what they are comparing is the strength of a model learned trained by supervised learning and a model trained by reinforcement learning so the supervised learning model is imitating human expert players so if you just get a huge amount of games played by expert players in the game of Go and you try to imitate them you are going to get better but then you

中文：而且这还算不上沉闷，极其 强大的玩家，以下是他们的表现 比较的是模型的强度 通过监督学习进行学习和训练 以及通过强化训练的模型 因此，监督式学习 该模型模仿人类专家玩家 所以如果你得到大量的 专家玩家玩的游戏 你玩围棋，并试图模仿他们。 你会好起来的，但是之后你

### 2:43:28–2:43:50

EN：top out and you never quite get better than some of the top top top players of in the game of Go like LEL so you're never going to reach there because you're just imitating human players you can't fundamentally go beyond a human player if you're just imitating human players but in a process of reinforcement learning is significantly more powerful in reinforcement learning for a game of Go it means that the

中文：达到顶峰，你永远无法真正进步。 比一些顶尖球员还要顶尖 在围棋游戏中，就像 LEL 一样，所以你是 永远也到不了那里，因为 你只是在模仿人类玩家而已。 从根本上来说，它无法超越人类的范畴。 如果你只是在模仿人类，那你就是个玩家。 玩家们，但在一个过程中 强化学习显著 在强化学习中更强大 在围棋比赛中，这意味着

### 2:43:50–2:44:15

EN：system is playing moves that empirically and statistically lead to win to winning the game and so alphago is a system where it kind of plays against it itself and it's using reinforcement learning to create rollouts so it's the exact same diagram here but there's no prompt it's just uh because there's no prompt it's just a fixed game of Go but it's trying out lots of solutions it's trying out lots

中文：系统正在采取经验表明有效的行动 从统计学角度来看，这会导致最终的胜利。 游戏，以及AlphaGo，都是一个系统。 它某种程度上是在与自身对抗。 它使用强化学习来 创造 推出方式，所以是完全相同的图表 这里没有提示，只有“呃”。 因为没有提示，所以它只是一个 围棋游戏已修复，但正在尝试 它正在尝试很多解决方案。

### 2:44:15–2:44:41

EN：of plays and then the games that lead to a win instead of a specific answer are reinforced they're they're made stronger and so um the system is learning basically the sequences of actions that empirically and statistically lead to winning the game and reinforcement learning is not going to be constrained by human performance and reinforcement learning can do significantly better and overcome even the top players like Lisa

中文：比赛以及由此引发的比赛 用胜利代替具体答案是 加固后，它们变得更坚固了。 所以，系统正在学习 基本上是指一系列动作 经验和统计结果表明 赢得比赛和加强 学习不会受到限制。 通过人类的表现和强化 学习可以做得更好，而且 甚至能战胜像丽莎这样的顶级选手。

### 2:44:41–2:45:01

EN：Dole and so uh probably they could have run this longer and they just chose to crop it at some point because this costs money but this is very powerful demonstration of reinforcement learning and we're only starting to kind of see hints of this diagram in larger language models for reasoning problems so we're not going to get too far by just imitating experts we need to go beyond

中文：多尔，所以，呃，他们可能可以…… 他们选择继续这样做。 因为这样会花费不少钱，所以最好在某个地方裁剪一下。 金钱，但这非常强大。 强化学习演示 我们才刚刚开始看到一些端倪。 更详细的语言中对此图的暗示 推理问题的模型，所以我们是 光靠这个是走不了多远的。 模仿专家，我们需要超越他们。

### 2:45:01–2:45:29

EN：that set up these like little game environments and get let let the system discover reasoning traces or like ways of solving problems uh that are unique and that uh just basically work well now on this aspect of uniqueness notice that when you're doing reinforcement learning nothing prevents you from veering off the distribution of how humans are playing the game and so when we go back to uh this alphao search

中文：这就像是在玩小游戏 环境并让系统 发现推理痕迹或类似方法 解决独特的问题 基本上就是这样。 好，现在来说说独特性的这个方面。 注意，当你这样做的时候 强化学习没有什么能阻止它 你避免偏离分布 人类是如何玩这场游戏的，等等。 当我们回到这个 alphao 搜索时

### 2:45:29–2:45:52

EN：here one of the suggested modifications is called move 37 and move 37 in alphao is referring to a specific point in time where alphago basically played a move that uh no human expert would play uh so the probability of this move uh to be played by a human player was evaluated to be about 1 in 10th ,000 so it's a very rare move but in retrospect it was

中文：以下是其中一项建议的修改 被称为第 37 步，在 alphao 中为第 37 步 指的是某个特定的时间点。 AlphaGo 基本上走了一步棋 呃，没有哪个人类专家会玩这个游戏。 这一举动的概率是 由人类玩家进行的游戏被评估 大约是万分之一，所以这是一个 非常罕见的举动，但事后看来是

### 2:45:52–2:46:19

EN：a brilliant move so alphago in the process of reinforcement learning discovered kind of like a strategy of playing that was unknown to humans and but is in retrospect uh brilliant I recommend this YouTube video um leis do versus alphao move 37 reactions and Analysis and this is kind of what it looked like when alphao played this move value that's a very that's a very surprising move I thought I thought it

中文：这是 AlphaGo 的一次精彩操作。 强化学习过程 发现有点像一种策略 人类从未体验过的游戏 但现在回想起来，这真是太棒了。 推荐这个 YouTube 视频 um leis do 对抗 alphao 移动 37 反应和 分析，这就是它的意义所在。 看起来像阿尔法奥玩这个游戏时的样子 移动 非常有价值的 出乎意料的举动，我以为我……

### 2:46:19–2:46:39

EN：was I thought it was a mistake when I see this move anyway so basically people are kind of freaking out because it's a it's a move that a human would not play that alphago played because in its training uh this move seemed to be a good idea it just happens not to be a kind of thing that a humans would would do and so that is again the

中文：我当时以为那是…… 我看到这一招时还是觉得错了。 基本上，人们都有点…… 退出，因为这是一个举动 人类不会玩AlphaGo玩的那种游戏。 因为在它的训练中，呃，这一招 看起来是个好主意，碰巧如此。 不应该成为人类的那种东西 会这么做，所以这又是……

### 2:46:39–2:47:00

EN：power of reinforcement learning and in principle we can actually see the equivalence of that if we continue scaling this Paradigm in language models and what that looks like is kind of unknown so so um what does it mean to solve problems in such a way that uh even humans would not be able to get how can you be better at reasoning or thinking than humans how can you go

中文：强化学习的力量以及 我们实际上可以看到这个原理 如果我们继续下去，那就等同于此。 在语言模型中扩展这种范式 而那看起来有点像…… 未知，所以，嗯，这是什么意思？ 以某种方式解决问题，呃 即使是人类也无法理解其中的原理 你的推理能力可以更强吗？ 比人类思考得更透彻，你怎么能去

### 2:47:00–2:47:24

EN：beyond just uh a thinking human like maybe it means discovering analogies that humans would not be able to uh create or maybe it's like a new thinking strategy it's kind of hard to think through uh maybe it's a holy new language that actually is not even English maybe it discovers its own language that is a lot better at thinking um because the model is unconstrained to even like stick with

中文：不仅仅是像人类那样思考 也许这意味着发现相似之处 人类将无法…… 创造，或者说是一种新的思维方式 制定策略有点难。 或许，这是一种神圣的新事物 甚至都算不上语言 英语或许会发现自己的 语言表达能力要好得多 思考中，因为模型是 不受约束地甚至喜欢坚持

### 2:47:24–2:47:45

EN：English uh so maybe it takes a different language to think in or it discovers its own language so in principle the behavior of the system is a lot less defined it is open to do whatever works and it is open to also slowly Drift from the distribution of its training data which is English but all of that can only be done if we have a very large

中文：英语，嗯，所以也许需要不同的方法。 用语言思考，或者它发现自己的语言 自己的语言，所以原则上 系统行为大大减少 它的定义是：可以做任何有效的事情。 而且它也可能慢慢地从……漂移。 其训练数据的分布 这是英语，但所有这些都可以 只有当我们拥有非常大的数量时才能这样做。

### 2:47:45–2:48:05

EN：diverse set of problems in which the these strategy can be refined and perfected and so that is a lot of the frontier LM research that's going on right now is trying to kind of create those kinds of prompt distributions that are large and diverse these are all kind of like game environments in which the llms can practice their thinking and uh it's kind of like writing you know these

中文：一系列不同的问题，其中 这些策略可以进一步完善， 已经完善，所以这其中有很多…… 正在进行的前沿LM研究 目前正在尝试创造某种东西。 那些类型的即时分配 它们种类繁多，体型庞大，这些都是很好的选择。 类似的游戏环境，其中 法学硕士可以练习他们的思维方式，呃…… 这有点像写你知道的这些

### 2:48:06–2:48:29

EN：practice problems we have to create practice problems for all of domains of knowledge and if we have practice problems and tons of them the models will be able to reinforcement learning reinforcement learn on them and kind of uh create these kinds of uh diagrams but in the domain of open thinking instead of a closed domain like game of Go there's one more section within reinforcement learning that I wanted to

中文：我们需要创建练习题 涵盖所有领域的练习题 知识，以及如果我们有实践经验的话。 模型存在大量问题。 将能够进行强化学习 强化学习，并从中学习，有点像 呃，创建这类图表，但是 相反，在开放思维领域。 像围棋这样的封闭领域 里面还有最后一部分 我想要的强化学习

## 20. reinforcement learning from human feedback (RLHF)（2:48:26–3:09:39）

### 2:48:29–2:48:53

EN：cover and that is that of learning in unverifiable domains so so far all of the problems that we've looked at are in what's called verifiable domains that is any candidate solution we can score very easily against a concrete answer so for example answer is three and we can very easily score these Solutions against the answer of three either we require the models to like box in their answers and then we just check

中文：涵盖范围，也就是学习的范围。 到目前为止，所有无法验证的域名 我们已经研究过的问题是： 这就是所谓的可验证域。 任何候选解决方案我们都能获得很高的分数。 很容易就能找到一个具体的答案，所以 例如，答案是三，我们可以非常 轻松地对这些解决方案进行评分 答案是三个 我们要么要求模型像盒子一样。 在他们的回答中，然后我们进行核对。

### 2:48:53–2:49:14

EN：for equality of whatever is in the box with the answer or you can also use uh kind of what's called an llm judge so the llm judge looks at a solution and it gets the answer and just basically scores the solution for whether it's consistent with the answer or not and llms uh empirically are good enough at the current capability that they can do this fairly reliably so we can apply

中文：为了使盒子里所有东西都相等。 用答案，或者你也可以用呃 有点像那种所谓的法学硕士法官。 法学硕士法官审视了一个解决方案，然后…… 得到答案，然后基本上 根据解决方案是否有效进行评分 与答案一致或不一致 llms 呃，从经验上看已经足够好了 他们目前的能力 这种方法相当可靠，所以我们可以应用

### 2:49:14–2:49:33

EN：those kinds of techniques as well in any case we have a concrete answer and we're just checking Solutions again against it and we can do this automatically with no kind of humans in the loop the problem is that we can't apply the strategy in what's called unverifiable domains so usually these are for example creative writing tasks like write a joke about Pelicans or write a poem or summarize a

中文：在任何情况下，这些技术也同样适用。 如果我们有确切的答案，我们 再次核对解决方案。 我们可以自动完成这项工作，无需任何操作。 问题在于，这类人身处问题之中。 问题在于我们无法应用该策略 所谓无法验证的域名，就是 通常这些都具有创意。 写作任务，例如写一个关于……的笑话 鹈鹕，或者写一首诗，或者总结一首诗

### 2:49:33–2:49:56

EN：paragraph or something like that in these kinds of domains it becomes harder to score our different solutions to this problem so for example writing a joke about Pelicans we can generate lots of different uh jokes of course that's fine for example we can go to chbt and we can get it to uh generate a joke about Pelicans uh so much stuff in their beaks because they don't bellan in

中文：段落或类似内容 这类领域就更难了。 为我们针对此问题的不同解决方案打分 例如，写笑话时会遇到问题。 关于鹈鹕，我们可以生成很多内容。 不同的笑话当然没问题 例如，我们可以去chbt，我们可以 让它生成一个关于……的笑话 鹈鹕嘴里叼着好多东西 因为他们不参与战斗

### 2:49:56–2:50:22

EN：backpacks what okay we can uh we can try something else why don't Pelicans ever pay for their drinks because they always B it to someone else haha okay so these models are not obviously not very good at humor actually I think it's pretty fascinating because I think humor is secretly very difficult and the model have the capability I think anyway in any case you could imagine creating lots of jokes

中文：背包什么 好的，我们可以试试别的办法。 为什么鹈鹕队从来不为他们的 因为他们总是喝饮料 哈哈，还有其他人。好的，这些模型 显然不太擅长幽默 实际上，我觉得这非常引人入胜。 因为我认为幽默本质上是非常 困难，而且该模型具有 我认为无论如何，这都是一种能力。 你可以想象自己创作很多笑话。

### 2:50:23–2:50:41

EN：the problem that we are facing is how do we score them now in principle we could of course get a human to look at all these jokes just like I did right now the problem with that is if you are doing reinforcement learning you're going to be doing many thousands of updates and for each update you want to be looking at say thousands of prompts and for each prompt you want to be

中文：我们面临的问题是如何 我们现在就可以给他们评分，原则上我们可以 当然要找个人来看一下所有情况。 这些笑话就像我刚才讲的一样 问题在于，如果你是 你正在进行强化学习 将会做成千上万次 更新，以及您希望的每次更新 比如说，要查看成千上万个提示。 对于每个提示，你都希望是

### 2:50:41–2:51:01

EN：potentially looking at looking at hundred or thousands of different kinds of generations and so there's just like way too many of these to look at and so um in principle you could have a human inspect all of them and score them and decide that okay maybe this one is funny and uh maybe this one is funny and this one is funny and we could train on them

中文：可能正在考虑查看 成百上千种不同的种类 一代又一代，所以就像…… 数量太多了，根本看不过来。 嗯，原则上你可以拥有一个人类 检查所有物品并评分， 决定好吧，也许这个挺搞笑的。 呃，也许这个挺搞笑的，还有这个 其中一个很有趣，我们可以拿它来训练。

### 2:51:01–2:51:23

EN：to get the model to become slightly better at jokes um in the context of pelicans at least um the problem is that it's just like way too much human time this is an unscalable strategy we need some kind of an automatic strategy for doing this and one sort of solution to this was proposed in this paper uh that introduced what's called reinforcement learning from Human feedback and so this was a paper from

中文：使模型略微 更擅长讲笑话，嗯，在……的语境下 鹈鹕至少……嗯，问题是…… 感觉就像人类时间太长了。 这是一个无法扩展的策略，我们需要 某种自动化策略 这样做是一种解决方案 本文提出了这一观点。 呃，那引入了所谓的 从人类身上学习强化学习 反馈，所以这是一篇来自……的论文

### 2:51:23–2:51:49

EN：open at the time and many of these people are now um co-founders in anthropic um and this kind of proposed a approach for uh basically doing reinforcement learning in unverifiable domains so let's take a look at how that works so this is the cartoon diagram of the core ideas involved so as I mentioned the native approach is if we just set Infinity human time we could just run RL in these domains just fine

中文：当时开放，而且其中很多都是这样的。 现在人们是联合创始人。 人为因素，以及这种提出的方​​案 基本上就是这么做的方法 强化学习在不可验证的 域名，所以我们来看看它是如何运作的。 所以，这就是它的卡通示意图。 所涉及的核心思想，所以我 提到原生方法，就是如果我们 只要设定无限的人类时间，我们就可以 在这些领域运行强化学习完全没问题。

### 2:51:49–2:52:10

EN：so for example we can run RL as usual if I have Infinity humans I would I just want to do and these are just cartoon numbers I want to do 1,000 updates where each update will be on 1,000 prompts and in for each prompt we're going to have 1,000 roll outs that we're scoring so we can run RL with this kind of a setup the problem is in the process of doing this

中文：例如，我们可以像往常一样运行强化学习程序。 我拥有无限的人类，我只想…… 想做的，这些只是卡通 我想进行 1000 次更新，其中 每次更新将涉及 1,000 个提示， 对于每个提示，我们都会有 我们正在对 1000 个推广项目进行评分，所以我们 在这种配置下可以运行强化学习。 问题就出在这个过程中。

### 2:52:10–2:52:32

EN：I will need to run one I will need to ask a human to evaluate a joke a total of 1 billion times and so that's a lot of people looking at really terrible jokes so we don't want to do that so instead we want to take the arlef approach so um in our Rel of approach we are kind of like the the core trick is that of indirection so we're going to

中文：我需要运行一个，我需要 请人对一个笑话进行总体评价 十亿倍，所以这很多。 人们看着非常糟糕的事情 开玩笑，所以我们不想那样做。 相反，我们想取 arlef。 所以，嗯，在我们的方法论中，我们 有点像核心技巧是 那是间接的，所以我们要……

### 2:52:32–2:52:56

EN：involve humans just a little bit and the way we cheat is that we basically train a whole separate neural network that we call a reward model and this neural network will kind of like imitate human scores so we're going to ask humans to score um roll we're going to then imitate human scores using a neural network and this neural network will become a kind of simulator of human

中文：只需稍微牵涉到人类， 我们作弊的方式就是我们基本上是在训练。 我们使用的完全独立的神经网络 调用奖励模型和这种神经 网络会有点像模仿人类 评分，所以我们要请人类来…… 得分 接下来我们将模仿人类的评分方式。 使用神经网络和这种神经网络 网络将成为一种模拟器 人类

### 2:52:56–2:53:17

EN：preferences and now that we have a neural network simulator we can do RL against it so instead of asking a real human we're asking a simulated human for their score of a joke as an example and so once we have a simulator we're often racist because we can query it as many times as we want to and it's all whole automatic process and we can now do

中文：偏好，现在我们有了 我们可以使用神经网络模拟器进行强化学习。 反对它，所以与其问一个真正的 我们是在向模拟人类提出要求 以笑话为例，他们的评分 所以一旦我们有了模拟器，我们通常 种族主义，因为我们可以像许多人一样质疑它 想来就来，而且一切都很完整 自动化流程，我们现在可以这样做了

### 2:53:17–2:53:36

EN：reinforcement learning with respect to the simulator and the simulator as you might expect is not going to be a perfect human but if it's at least statistically similar to human judgment then you might expect that this will do something and in practice indeed uh it does so once we have a simulator we can do RL and everything works great so let me show you a cartoon diagram a little

中文：强化学习 模拟器和模拟器作为你 可能预期不会是 完美的人，但至少 与人类判断在统计学上相似 那么你可能会认为这样做会有效。 某种东西，实际上确实如此。 一旦我们有了模拟器，我们就可以这样做了。 进行 RL 测试，一切进展顺利，所以就这么做吧。 我给你展示一下简略的卡通图。

### 2:53:36–2:53:56

EN：bit of what this process looks like although the details are not 100 like super important it's just a core idea of how this works so here I have a cartoon diagram of a hypothetical example of what training the reward model would look like so we have a prompt like write a joke about picans and then here we have five separate roll outs so these are all five different jokes just like

中文：这个过程大概是这样的 虽然细节并非百分之百一样 非常重要，这只是一个核心理念 这是怎么回事？我这里有个卡通图。 假设示例的示意图 训练奖励模型会是什么样的呢？ 看起来我们有一个类似“写”的提示 一个关于黑皮诺的笑话，然后我们…… 有五个独立的推广计划，所以这些 这五个笑话都不一样，就像……

### 2:53:56–2:54:20

EN：this one now the first thing we're going to do is we are going to ask a human to uh order these jokes from the best to worst so this is uh so here this human thought that this joke is the best the funniest so number one joke this is number two joke number three joke four and five so this is the worst joke we're asking humans to order instead of

中文：这是我们首先要去的地方 我们要做的就是请一个人来做这件事 呃，按最佳顺序排列这些笑话 最糟糕的是，这就是……呃，所以这里这个人 我觉得这个笑话是最好的 这是最搞笑的笑话，排名第一！ 第二条笑话 第三条笑话 第四条 五，所以这是最糟糕的笑话 我们要求人类下单，而不是……

### 2:54:20–2:54:40

EN：give scores directly because it's a bit of an easier task it's easier for a human to give an ordering than to give precise scores now that is now the supervision for the model so the human has ordered them and that is kind of like their contribution to the training process but now separately what we're going to do is we're going to ask a reward model uh about its scoring of

中文：直接给出分数，因为这有点 对于一项较简单的任务来说，它就更容易了。 人类下达命令比给予更重要 现在就是精确的分数了 对模型进行监督，以便人类 已经订购了，这有点…… 例如他们对训练的贡献 流程，但现在分开来说，我们正在做什么 接下来我们要问的是一个 奖励模型，嗯，关于它的评分

### 2:54:40–2:55:07

EN：these jokes now the reward model is a whole separate neural network completely separate neural net um and it's also probably a transform uh but it's not a language model in the sense that it generates diverse language Etc it's just a scoring model so the reward model will take as an input The Prompt number one and number two a candidate joke so um those are the two inputs that go into the reward model so

中文：这些笑话现在奖励模式是 完全独立的神经网络 独立的神经网络，嗯，而且它也是 可能是一种转变 呃，但它并不是语言模型。 它给人一种感觉，即它能产生多样化的语言 等等，它只是一个评分模型，所以 奖励模型将以以下内容作为输入： 提示一和提示二 候选人笑话，嗯，就是这两个。 输入到奖励模型中的参数

### 2:55:07–2:55:27

EN：here for example the reward model would be taken this prompt and this joke now the output of a reward model is a single number and this number is thought of as a score and it can range for example from Z to one so zero would be the worst score and one would be the best score so here are some examples of what a hypothetical reward model at some stage

中文：例如，这里的奖励模型会 现在就接受这个提示和这个笑话吧 奖励模型的输出是一个单一值。 数字，而这个数字被认为是 分数可以有多种范围，例如 从 Z 到 1，所以 0 是最糟糕的。 得分，1 分最高。 以下是一些例子，说明什么是 假设奖励模型在某个阶段

### 2:55:27–2:55:51

EN：in the training process would give uh s scoring to these jokes so 0.1 is a very low score 08 is a really high score and so on and so now um we compare the scores given by the reward model with uh the ordering given by the human and there's a precise mathematical way to actually calculate this uh basically set up a loss function and calculate a kind

中文：在培训过程中会给予呃 给这些笑话打分，所以 0.1 是一个非常低的分数。 低分08其实是一个非常高的分数， 如此往复，现在我们来比较一下。 由奖励模型给出的分数（呃） 人类所给出的顺序和 有一种精确的数学方法来…… 实际上，计算这个基本上是这样的 建立损失函数并计算一种

### 2:55:51–2:56:11

EN：of like a correspondence here and uh update a model based on it but I just want to give you the intuition which is that as an example here for this second joke the the human thought that it was the funniest and the model kind of agreed right 08 is a relatively high score but this score should have been even higher right so after an update we would expect that maybe this score

中文：这里就像一封信，呃…… 基于此更新模型，但我只是 想给你这种直觉，那就是 举个例子，这里是第二个例子。 人类认为这是个笑话 最搞笑的，也是模范型的 同意，08 是一个相对较高的值。 但这个分数应该是 更新后，我们甚至更高了。 可能会预期这个分数

### 2:56:11–2:56:33

EN：should have been will actually grow after an update of the network to be like say 081 or something um for this one here they actually are in a massive disagreement because the human thought that this was number two but here the the score is only 0.1 and so this score needs to be much higher so after an update on top of this um kind of a supervision this might

中文：应该会真正成长 网络更新后， 例如 081 或 嗯，这个他们 实际上，他们之间存在巨大分歧。 因为人类认为这是 第二名，但这里的比分是 只有 0.1，所以这个分数需要是 更新后，价格要高得多。 这嗯，某种程度上的监督，这可能

### 2:56:33–2:56:54

EN：grow a lot more like maybe it's 0.15 or something like that um and then here the human thought that this one was the worst joke but here the model actually gave it a fairly High number so you might expect that after the update uh this would come down to maybe 3 3.5 or something like that so basically we're doing what we did before we're slightly nudging the predictions

中文：增长幅度可能更大，比如达到 0.15 或 类似 嗯，然后这里是人类的思想 这是最烂的笑话，但 这里，模型实际上给了它一个相当 数字很​​高，所以你可能会预料到这一点。 更新之后，呃，这个就会下降。 大概3、3.5之类的吧 基本上，我们做的和以前一样。 我们稍微调整了一下预测结果。

### 2:56:54–2:57:20

EN：from the models using a neural network training process and we're trying to make the reward model scores be consistent with human ordering and so um as we update the reward model on human data it becomes better and better simulator of the scores and orders uh that humans provide and then becomes kind of like the the neural the simulator of human preferences which we can then do RL

中文：来自使用神经网络的模型 训练 流程，我们正在努力使 奖励模型得分应与 人类 排序等等，嗯，随着我们更新 基于人类数据的奖励模型会变成 越来越好的模拟器 人类提供的分数和订单 然后就变得有点像…… 人类神经模拟器 我们可以根据偏好进行强化学习

### 2:57:20–2:57:39

EN：against but critically we're not asking humans one billion times to look at a joke we're maybe looking at th000 prompts and five roll outs each so maybe 5,000 jokes that humans have to look at in total and they just give the ordering and then we're training the model to be consistent with that ordering and I'm skipping over the mathematical details but I just want you to understand a high

中文：反对，但关键是我们并没有要求 人类看了十亿遍 开玩笑说，我们可能正在看着 th000 提示和五次推广，所以也许 人类不得不看的5000个笑话 总共，他们只是给出排序结果。 然后我们训练模型，使其能够 与该顺序一致，我是 略过数学细节 但我只是想让你明白高

### 2:57:39–2:58:05

EN：level idea that uh this reward model is do is basically giving us this scour and we have a way of training it to be consistent with human orderings and that's how rhf works okay so that is the rough idea we basically train simulators of humans and RL with respect to those simulators now I want to talk about first the upside of reinforcement learning from Human feedback the first thing is that this

中文：这个想法的层次在于，呃，这个奖励模型是 基本上就是给我们进行这种彻底的清洗和 我们有办法训练它成为 符合人类的秩序 这就是射频的工作原理，好的。 我们基本上训练的大致思路是 人类模拟器和强化学习 致那些 现在我想谈谈模拟器。 首先是加固的优势 向人类学习 首先反馈是这样的

### 2:58:05–2:58:28

EN：allows us to run reinforcement learning which we know is incredibly powerful kind of set of techniques and it allows us to do it in arbitrary domains and including the ones that are unverifiable so things like summarization and poem writing joke writing or any other creative writing really uh in domains outside of math and code Etc now empirically what we see when we actually apply rhf is that this is a way

中文：使我们能够运行强化学习 我们知道它威力无比。 一系列技术，它允许 让我们能够在任意领域做到这一点，并且 包括那些无法核实的。 所以像总结和诗歌之类的东西。 写笑话、写段子或其他任何内容 创意写作在很多领域都非常…… 除了数学和代码之外 等等，现在根据经验，我们看到当我们 实际上，应用 RHF 的方法就是如此。

### 2:58:28–2:58:47

EN：to improve the performance of the model and uh I have a top answer for why that might be but I don't actually know that it is like super well established on like why this is you can empirically observe that when you do rhf correctly the models you get are just like a little bit better um but as to why is I think like not as clear so here's my

中文：为了提高模型的性能 嗯，我有一个最佳答案来解释为什么会这样。 也许是，但我并不确定。 它就像是超级成熟的 比如为什么会这样，你可以通过经验来证明。 注意，当你正确地进行 rhf 操作时。 你得到的模型就像…… 稍微好一点了，嗯，但是为什么呢？ 感觉不太清楚，所以这是我的解释。

### 2:58:47–2:59:18

EN：best guess my best guess is that this is possibly mostly due to the discriminator generator Gap what that means is that in many cases it is significantly easier to discriminate than to generate for humans so in particular an example of this is um in when we do supervised fine-tuning right sft we're asking humans to generate the ideal assistant response and in many cases here um as I've shown it uh the

中文：我最好的猜测是，这是 可能主要归因于歧视者 发电机 这意味着在许多方面存在差距。 在某些情况下，这样做要容易得多。 与其说是为了人类而进行歧视，不如说是为了人类而进行歧视。 具体来说，一个例子是： 嗯，当我们进行监督式微调时 正确的 我们要求人类生成…… 理想的助手响应以及许多 这里的案例，嗯，正如我所展示的，嗯……

### 2:59:18–2:59:40

EN：ideal response is very simple to write but in many cases might not be so for example in summarization or poem writing or joke writing like how are you as a human assist as a human labeler um supposed to give the ideal response in these cases it requires creative human writing to do that and so rhf kind of sidesteps this because we get um we get to ask people a significantly easier

中文：理想的回答非常简单。 但在许多情况下，情况可能并非如此。 总结或诗歌写作示例 或者写一些玩笑话，比如“你好吗？” 作为人类贴标签者的人类协助嗯 应该给出理想的回应 这些情况需要有创造力的人 写这篇文章就是为了做到这一点，所以 rhf 有点像 避开这个问题，因为我们得到了……我们得到了 问别人一个更容易的问题

### 2:59:40–3:00:02

EN：question as a data labelers they're not asked to write poems directly they're just given five poems from the model and they're just asked to order them and so that's just a much easier task for a human labeler to do and so what I think this allows you to do basically is it um it kind of like allows a lot more higher accuracy data because we're not asking

中文：作为数据标注者，他们提出的问题是： 被要求直接写诗时，他们是 刚刚从模型中选取了五首诗， 他们只是被要求下单而已，就这样。 这对于一个……来说，无疑是一项更容易的任务。 人工标注员来做，所以我的想法是…… 这基本上可以让你做到……嗯 它有点像是允许更高的 因为我们没有询问准确率数据，所以不需要这些数据。

### 3:00:02–3:00:25

EN：people to do the generation task which can be extremely difficult like we're not asking them to do creative writing we're just trying to get them to distinguish between creative writings and uh find the ones that are best and that is the signal that humans are providing just the ordering and that is their input into the system and then the system in rhf just discovers the kinds of responses that would be graded well

中文：让人们完成生成任务， 这可能非常困难，就像我们一样 不要求他们进行创意写作 我们只是想让他们…… 区分创意写作 然后找到最好的那些。 这是人类存在的信号 仅提供订购服务，仅此而已。 他们将信息输入系统，然后 rhf 系统中仅发现各种类型 能够获得高分的回答

### 3:00:26–3:00:54

EN：by humans and so that step of indirection allows the models to become a bit better so that is the upside of our LF it allows us to run RL it empirically results in better models and it allows uh people to contribute their supervision uh even without having to do extremely difficult tasks um in the case of writing ideal responses unfortunately our HF also comes with significant downsides and so um the main one is that

中文：由人类完成，因此这一步骤 间接性使得模型能够成为 情况稍微好转了一些，这是好处。 我们的 LF 允许我们运行 RL 经验结果表明，这些方法可以得出更好的模型。 它允许人们贡献他们的 监督，即使不必真的去做 极其困难的任务，嗯，在这种情况下 可惜的是，很难写出理想的回应。 我们的HF也具有显著的优势。 缺点，最主要的一点是……

### 3:00:54–3:01:15

EN：basically we are doing reinforcement learning not with respect to humans and actual human judgment but with respect to a lossy simulation of humans right and this lossy simulation could be misleading because it's just a it's just a simulation right it's just a language model that's kind of outputting scores and it might not perfectly reflect the opinion of an actual human with an actual brain in all the possible

中文：我们基本上是在进行加固。 学习并非出于对人类的尊重，而是…… 出于对人类判断的尊重 对人类权利的有损模拟 这种有损模拟可能是 具有误导性，因为它只是一个…… 模拟，对吧，它只是一种语言 该模型会输出分数 但这可能无法完全反映…… 一个真实人类的观点 真正的大脑在所有可能的范围内

### 3:01:15–3:01:43

EN：different cases so that's number one which is actually something even more subtle and devious going on that uh really dramatically holds back our LF as a technique that we can really scale to significantly um kind of Smart Systems and that is that reinforcement learning is extremely good at discovering a way to game the model to game the simulation so this reward model that we're constructing here that gives the course

中文：情况各不相同，这是第一点。 实际上，这甚至更甚。 事情进展得既微妙又狡猾，呃…… 真的 极大地阻碍了我们LF的运作 我们可以真正扩展的技术 显著的智能​​系统 这就是强化学习 非常擅长寻找方法 操纵模型以操纵模拟 所以，我们采用的这种奖励模式是 这里构建的课程

### 3:01:43–3:02:08

EN：these models are Transformers these Transformers are massive neurals they have billions of parameters and they imitate humans but they do so in a kind of like a simulation way now the problem is that these are massive complicated systems right there's a billion parameters here that are outputting a single score it turns out that there are ways to gain these models you can find kinds of inputs that were not part of their

中文：这些模型是变形金刚。 变形金刚是巨大的神经元，它们 拥有数十亿个参数，而且它们 它们模仿人类，但它们以一种……的方式进行。 现在的问题就像模拟方式一样。 这些都是极其复杂的问题。 那里有十亿个系统。 这里输出的参数是 单身的 得分方式原来是有的 要获得这些模型，您可以找到各种 那些并非他们自身组成部分的投入

### 3:02:08–3:02:31

EN：training set and these inputs inexplicably get very high scores but in a fake way so very often what you find if you run our lch for very long so for example if we do 1,000 updates which is like say a lot of updates you might expect that your jokes are getting better and that you're getting like real bangers about Pelicans but that's not EXA exactly what happens what happens is

中文：训练集和这些输入 莫名其妙地获得非常高的分数，但在 虚假的方式，所以你经常会发现 如果你长时间运行我们的lch，那么对于 例如，如果我们进行 1,000 次更新，那就是 比如说，你可能会收到很多更新。 做好心理准备，你的笑话可能会被嘲笑。 更好，而且你越来越像真的了。 关于鹈鹕队的劲爆歌曲，但这并非事实。 EXA 到底发生了什么？发生了什么？

### 3:02:31–3:02:50

EN：that uh in the first few hundred steps the jokes about Pelicans are probably improving a little bit and then they actually dramatically fall off the cliff and you start to get extremely nonsensical results like for example you start to get um the top joke about Pelicans starts to be the and this makes no sense right like when you look at it why should this be a top

中文：呃，在最初的几百步里 关于鹈鹕的笑话可能 情况略有好转，然后他们 实际上，他猛地从悬崖上摔了下来。 然后你开始变得极其 例如，你这样的结果毫无意义。 开始明白关于……的那个最搞笑的笑话 鹈鹕队开始成为 这完全说不通，就像…… 你看看，为什么这会成为榜首？

### 3:02:50–3:03:12

EN：joke but when you take the the and you plug it into your reward model you'd expect score of zero but actually the reward model loves this as a joke it will tell you that the the the theth is a score of 1. Z this is a top joke and this makes no sense right but it's because these models are just simulations of humans and they're massive neural lots and you can find

中文：开玩笑，但当你拿走那个和你 把它加入你的奖励模型中，你就会…… 预期得分为零，但实际上 奖励模型很喜欢这个玩笑 会告诉你，这个是 得分1分。Z，这真是个绝妙的笑话。 这听起来毫无道理，对吧？但事实就是如此。 因为这些模型只是 人类模拟，它们是 大量的神经活动，你可以找到

### 3:03:12–3:03:32

EN：inputs at the bottom that kind of like get into the part of the input space that kind of gives you nonsensical results these examples are what's called adversarial examples and I'm not going to go into the topic too much but these are adversarial inputs to the model they are specific little inputs that kind of go between the nooks and crannies of the model and give nonsensical results at

中文：底部的输入口有点像 进入输入空间的这一部分 那会给你带来一些毫无意义的东西。 这些例子的结果就是所谓的 对抗样本，我不会去 不想在这个话题上花费太多笔墨，但是…… 它们是对模型的对抗性输入。 是一些特定的、细微的输入，它们有点像 穿梭于各个角落和缝隙之间 模型并给出毫无意义的结果

### 3:03:32–3:03:51

EN：the top now here's what you might imagine doing you say okay the the the is obviously not score of one um it's obviously a low score so let's take the the the the the let's add it to the data set and give it an ordering that is extremely bad like a score of five and indeed your model will learn that the D should have a very low score and it will

中文：现在最棒的是，你可能会…… 想象一下，你说好的，那 显然不是一分，嗯，是 显然分数很低，所以我们来看看 让我们把它添加到数据中。 设置并赋予它一个顺序，即 非常糟糕，比如五分。 事实上，你的模型会学习到D

### 3:03:51–3:04:14

EN：give it score of zero the problem is that there will always be basically infinite number of nonsensical adversarial examples hiding in the model if you iterate this process many times and you keep adding nonsensical stuff to your reward model and giving it very low scores you can you'll never win the game uh you can do this many many rounds and reinforcement learning if you run it long enough will always find a way to

中文：设置并赋予它一个顺序，即 非常糟糕，比如五分。 事实上，你的模型会学习到D

### 3:04:14–3:04:42

EN：gain the model it will discover adversarial examples it will get get really high scores uh with nonsensical results and fundamentally this is because our scoring function is a giant neural nut and RL is extremely good at finding just the ways to trick it uh so long story short you always run rhf put for maybe a few hundred updates the model is getting better and then you have to crop it and you are done you

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:04:42–3:05:06

EN：can't run too much against this reward model because the optimization will start to game it and you basically crop it and you call it and you ship it um and uh you can improve the reward model but you kind of like come across these situations eventually at some point so rhf basically what I usually say is that RF is not RL and what I mean by that is

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:05:06–3:05:27

EN：I mean RF is RL obviously but it's not RL in the magical sense this is not RL that you can run indefinitely these kinds of problems like where you are getting con correct answer you cannot gain this as easily you either got the correct answer or you didn't and the scoring function is much much simpler you're just looking at the boxed area and seeing if the result is

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:05:27–3:05:50

EN：correct so it's very difficult to gain these functions but uh gaming a reward model is possible now in these verifiable domains you can run RL indefinitely you could run for tens of thousands hundreds of thousands of steps and discover all kinds of really crazy strategies that we might not even ever think about of Performing really well for all these problems in the game of Go there's no way to to beat to basically

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:05:50–3:06:11

EN：game uh the winning of a game or the losing of a game we have a perfect simulator we know all the different uh where all the stones are placed and we can calculate uh whether someone has won or not there's no way to gain that and so you can do RL indefinitely and you can eventually be beat even leol but with models like this which are gameable

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:06:11–3:06:36

EN：you cannot repeat this process indefinitely so I kind of see rhf as not real RL because the reward function is gameable so it's kind of more like in the realm of like little fine-tuning it's a little it's a little Improvement but it's not something that is fundamentally set up correctly where you can insert more compute run for longer and get much better and magical results so it's it's uh it's not RL in that

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:06:36–3:06:57

EN：sense it's not RL in the sense that it lacks magic um it can find you in your model and get a better performance and indeed if we go back to chat GPT the GPT 40 model has gone through rhf because it works well but it's just not RL in the same sense rlf is like a little fine tune that slightly improves your model is maybe like the way I would think

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:06:57–3:07:21

EN：about it okay so that's most of the technical content that I wanted to cover I took you through the three major stages and paradigms of training these models pre-training supervised fine tuning and reinforcement learning and I showed you that they Loosely correspond to the process we already use for teaching children and so in particular we talked about pre-training being sort of like the basic knowledge acquisition of reading Exposition supervised fine

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:07:21–3:07:45

EN：tuning being the process of looking at lots and lots of worked examples and imitating experts and practice problems the only difference is that we now have to effectively write textbooks for llms and AIS across all the disciplines of human knowledge and also in all the cases where we actually would like them to work like code and math and you know basically all the other disciplines so we're in the process of writing

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:07:45–3:08:08

EN：textbooks for them refining all the algorithms that I've presented on the high level and then of course doing a really really good job at the execution of training these models at scale and efficiently so in particular I didn't go into too many details but these are extremely large and complicated distributed uh sort of um jobs that have to run over tens of thousands or even hundreds of thousands

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:08:08–3:08:31

EN：of gpus and the engineering that goes into this is really at the stateof the art of what's possible with computers at that scale so I didn't cover that aspect too much but um this is very kind of serious and they were underlying all these very simple algorithms ultimately now I also talked about sort of like the theory of mind a little bit of these models and the thing I want you

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:08:31–3:08:52

EN：to take away is that these models are really good but they're extremely useful as tools for your work you shouldn't uh sort of trust them fully and I showed you some examples of that even though we have mitigations for hallucinations the models are not perfect and they will hallucinate still it's gotten better over time and it will continue to get better but they can hallucinate in other words in in

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:08:52–3:09:14

EN：addition to that I covered kind of like what I call the Swiss cheese uh sort of model of llm capabilities that you should have in your mind the models are incredibly good across so many different disciplines but then fail randomly almost in some unique cases so for example what is bigger 9.11 or 9.9 like the model doesn't know but simultaneously it can turn around and solve Olympiad questions and so this is

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:09:14–3:09:38

EN：a hole in the Swiss cheese and there are many of them and you don't want to trip over them so don't um treat these models as infallible models check their work use them as tools use them for inspiration use them for the first draft but uh work with them as tools and be ultimately respons responsible for the you know product of your work and that's roughly what I wanted to

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:09:38–3:09:56

EN：talk about this is how they're trained and this is what they are let's now turn to what are some of the future capabilities of these models uh probably what's coming down the pipe and also where can you find these models I have a few blow points on some of the things that you can expect coming down the pipe the first thing you'll notice is that the models will very rapidly become

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

## 21. preview of things to come（3:09:39–3:15:15）

### 3:09:56–3:10:19

EN：multimodal everything I talked about above concerned text but very soon we'll have llms that can not just handle text but they can also operate natively and very easily over audio so they can hear and speak and also images so they can see and paint and we're already seeing the beginnings of all of this uh but this will be all done natively inside inside the language model and this will

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:10:19–3:10:41

EN：enable kind of like natural conversations and roughly speaking the reason that this is actually no different from everything we've covered above is that as a baseline you can tokenize audio and images and apply the exact same approaches of everything that we've talked about above so it's not a fundamental change it's just uh it's just a to we have to add some tokens so as an example for tokenizing audio we

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:10:41–3:11:03

EN：can look at slices of the spectrogram of the audio signal and we can tokenize that and just add more tokens that suddenly represent audio and just add them into the context windows and train on them just like above the same for images we can use patches and we can separately tokenize patches and then what is an image an image is just a sequence of tokens and this actually

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:11:03–3:11:24

EN：kind of works and there's a lot of early work in this direction and so we can just create streams of tokens that are representing audio images as well as text and interpers them and handle them all simultaneously in a single model so that's one example of multimodality uh second something that people are very interested in is currently most of the work is that we're handing individual tasks to the

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:11:24–3:11:46

EN：models on kind of like a silver platter like please solve this task for me and the model sort of like does this little task but it's up to us to still sort of like organize a coherent execution of tasks to perform jobs and the models are not yet at the capability required to do this in a coherent error correcting way over long periods of time so they're not

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:11:46–3:12:07

EN：able to fully string together tasks to perform these longer running jobs but they're getting there and this is improving uh over time but uh probably what's going to happen here is we're going to start to see what's called agents which perform tasks over time and you you supervise them and you watch their work and they come up to once in a while report progress and so on so we're

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:12:07–3:12:27

EN：going to see more long running agents uh tasks that don't just take you know a few seconds of response but many tens of seconds or even minutes or hours over time uh but these uh models are not infallible as we talked about above so all of this will require supervision so for example in factories people talk about the human to robot ratio uh for automation I think we're going to see

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:12:27–3:12:53

EN：something similar in the digital space where we are going to be talking about human to agent ratios where humans becomes a lot more supervisors of agent tasks um in the digital domain uh next um I think everything is going to become a lot more pervasive and invisible so it's kind of like integrated into the tools and everywhere um and in addition kind of like computer using so right now these models aren't

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:12:53–3:13:14

EN：able to take actions on your behalf but I think this is a separate bullet point um if you saw chpt launch the operator then uh that's one early example of that where you can actually hand off control to the model to perform you know keyboard and mouse actions on your behalf so that's also something that that I think is very interesting the last point I have here is just a general

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:13:14–3:13:34

EN：comment that there's still a lot of research to potentially do in this domain main one example of that uh is something along the lines of test time training so remember that everything we've done above and that we talked about has two major stages there's first the training stage where we tune the parameters of the model to perform the tasks well once we get the parameters we fix them and then we deploy the model

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:13:34–3:13:56

EN：for inference from there the model is fixed it doesn't change anymore it doesn't learn from all the stuff that it's doing a test time it's a fixed um number of parameters and the only thing that is changing is now the token inside the context windows and so the only type of learning or test time learning that the model has access to is the in context learning of its uh kind of like

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:13:56–3:14:16

EN：uh dynamically adjustable context window depending on like what it's doing at test time so but I think this is still different from humans who actually are able to like actually learn uh depending on what they're doing especially when you sleep for example like your brain is updating your parameters or something like that right so there's no kind of equivalent of that currently in these models and tools so there's a lot of

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:14:16–3:14:37

EN：like um more wonky ideas I think that are to be explored still and uh in particular I think this will be necessary because the context window is a finite and precious resource and especially once we start to tackle very long running multimodal tasks and we're putting in videos and these token windows will basically start to grow extremely large like not thousands or even hundreds of thousands but

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:14:37–3:14:58

EN：significantly beyond that and the only trick uh the only kind of trick we have Avail to us right now is to make the context Windows longer but I think that that approach by itself will will not will not scale to actual long running tasks that are multimodal over time and so I think new ideas are needed in some of those disciplines um in some of those kind of cases in the main where these

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:14:58–3:15:16

EN：tasks are going to require very long contexts so those are some examples of some of the things you can um expect coming down the pipe let's now turn to where you can actually uh kind of keep track of this progress and um you know be up to date with the latest and grest of what's happening in the field so I would say the three resources that I

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

## 22. keeping track of LLMs（3:15:15–3:18:34）

### 3:15:16–3:15:40

EN：have consistently used to stay up to date are number one El Marina uh so let me show you El Marina this is basically an llm leader board and it ranks all the top models and the ranking is based on human comparisons so humans prompt these models and they get to judge which one gives a better answer they don't know which model is which they're just looking at which model is the better

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:15:40–3:15:59

EN：answer and you can calculate a ranking and then you get some results and so what you can hear is what you can see here is the different organizations like Google Gemini for example that produce these models when you click on any one of these it takes you to the place where that model is hosted and then here we see Google is currently on top with open AI right

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:15:59–3:16:18

EN：behind here we see deep seek in position number three now the reason this is a big deal is the last column here you see license deep seek is an MIT license model it's open weights anyone can use these weights uh anyone can download them anyone can host their own version of Deep seek and they can use it in what whatever way they like and so it's not a

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:16:18–3:16:40

EN：proprietary model that you don't have access to it's it's basically an open weight release and so this is kind of unprecedented that a model this strong was released with open weights so pretty cool from the team next up we have a few more models from Google and open Ai and then when you continue to scroll down you start to see some other Usual Suspects so xai here anthropic with son

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:16:40–3:17:08

EN：it uh here at number 14 and um then meta with llama over here so llama similar to deep seek is an open weights model and so uh but it's down here as opposed to up here now I will say that this leaderboard was really good for a long time I do think that in the last few months it's become a little bit gamed um and I don't trust it as much as

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:17:08–3:17:30

EN：I used to I think um just empirically I feel like a lot of people for example are using a Sonet from anthropic and that it's a really good model so but that's all the way down here um in number 14 and conversely I think not as many people are using Gemini but it's racking really really high uh so I think use this as a first pass uh but uh sort

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:17:30–3:17:50

EN：of try out a few of the models for your tasks and see which one performs better the second thing that I would point to is the uh AI news uh newsletter so AI news is not very creatively named but it is a very good newsletter produced by swix and friends so thank you for maintaining it and it's been very helpful to me because it is extremely comprehensive so if you

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:17:50–3:18:09

EN：go to archives uh you see that it's produced almost every other day and um it is very comprehensive and some of it is written by humans and curated by humans but a lot of it is constructed automatically with llms so you'll see that these are very comprehensive and you're probably not missing anything major if you go through it of course you're probably not going to go through

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:18:09–3:18:29

EN：it because it's so long but I do think that these summaries all the way up top are quite good and I think have some human oversight uh so this has been very helpful to me and the last thing I would point to is just X and Twitter uh a lot of um AI happens on X and so I would just follow people who you like and trust and get all your latest and

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:18:29–3:18:47

EN：greatest uh on X as well so those are the major places that have worked for me over time and finally a few words on where you can find the models and where can you use them so the first one I would say is for any of the biggest proprietary models you just have to go to the website of that LM provider so for example for open a that's uh chat

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

## 23. where to find LLMs（3:18:34–3:21:46）

### 3:18:47–3:19:10

EN：I believe actually works now uh so that's for open AI now for or you know for um for Gemini I think it's gem. google.com or AI Studio I think they have two for some reason that I don't fly understand no one does um for the open weights models like deep SE CL Etc you have to go to some kind of an inference provider of LMS so my favorite one is together

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:19:10–3:19:29

EN：together. a and I showed you that when you go to the playground of together. a then you can sort of pick lots of different models and all of these are open models of different types and you can talk to them here as an example um now if you'd like to use a base model like um you know a base model then this is where I think it's not as

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:19:29–3:19:49

EN：common to find base models even on these inference providers they are all targeting assistants and chat and so I think even here I can't I couldn't see base models here so for base models I usually go to hyperbolic because they serve my llama 3.1 base and I love that model and you can just talk to it here so as far as I know this is this is a

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:19:49–3:20:09

EN：good place for a base model and I wish more people hosted base models because they are useful and interesting to work with in some cases finally you can also take some of the models that are smaller and you can run them locally and so for example deep seek the biggest model you're not going to be able to run locally on your MacBook but there are smaller versions of the deep seek model

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:20:09–3:20:29

EN：that are what's called distilled and then also you can run these models at smaller Precision so not at the native Precision of for example fp8 on deep seek or you know bf16 llama but much much lower than that um and don't worry if you don't fully understand those details but you can run smaller versions that have been distilled and then at even lower precision and then you can

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:20:29–3:20:48

EN：fit them on your uh computer and so you can actually run pretty okay models on your laptop and my favorite I think place I go to usually is LM studio uh which is basically an app you can get and I think it kind of actually looks really ugly and it's I don't like that it shows you all these models that are basically not that useful like everyone

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:20:48–3:21:08

EN：just wants to run deep seek so I don't know why they give you these 500 different types of models they're really complicated to search for and you have to choose different distillations and different uh precisions and it's all really confusing but once you actually understand how it works and that's a whole separate video then you can actually load up a model like here I loaded up a llama 3 uh2 instruct 1

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:21:08–3:21:28

EN：billion and um you can just talk to it so I ask for Pelican jokes and I can ask for another one and it gives me another one Etc all of this that happens here is locally on your computer so we're not actually going to anywhere anyone else this is running on the GPU on the MacBook Pro so that's very nice and you can then eject the model when you're

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:21:28–3:21:47

EN：done and that frees up the ram so LM studio is probably like my favorite one even though I don't I think it's got a lot of uiux issues and it's really geared towards uh professionals almost uh but if you watch some videos on YouTube I think you can figure out how to how to use this interface uh so those are a few words on where to find them so let me now loop

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

## 24. grand summary（3:21:46–3:31:23）

### 3:21:47–3:22:10

EN：back around to where we started the question was when we go to chashi pta.com and we enter some kind of a query and we hit go what exactly is happening here what are we seeing what are we talking to how does this work and I hope that this video gave you some appreciation for some of the under the hood details of how these models are trained and what this is that is coming

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:22:10–3:22:34

EN：back so in particular we now know that your query is taken and is first chopped up into tokens so we go to to tick tokenizer and here where is the place in the in the um sort of format that is for the user query we basically put in our query right there so our query goes into what we discussed here is the conversation protocol format which is

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:22:34–3:23:00

EN：this way that we maintain conversation objects so this gets inserted there and then this whole thing ends up being just a token sequence a onedimensional token sequence under the hood so Chachi PT saw this token sequence and then when we hit go it basically continues appending tokens into this list it continues the sequence it acts like a token autocomplete so in particular it gave us this response so we can basically just

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:23:00–3:23:21

EN：put it here and we see the tokens that it continued uh these are the tokens that it continued with roughly now the question becomes okay why are these the tokens that the model responded with what are these tokens where are they coming from uh what are we talking to and how do we program this system and so that's where we shifted gears and we talked about the

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:23:21–3:23:44

EN：under thehood pieces of it so the first stage of this process and there are three stages is the pre-training stage which fundamentally has to do with just knowledge acquisition from the internet into the parameters of this neural network and so the neural net internalizes a lot of Knowledge from the internet but where the personality really comes in is in the process of supervised fine-tuning here and so what

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:23:44–3:24:08

EN：what happens here is that basically the a company like openai will curate a large data set of conversations like say 1 million conversation across very diverse topics and there will be conversations between a human and an assistant and even though there's a lot of synthetic data generation used throughout this entire process and a lot of llm help and so on fundamentally this is a human data curation task with lots

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:24:08–3:24:34

EN：of humans involved and in particular these humans are data labelers hired by open AI who are given labeling instructions that they learn and they task is to create ideal assistant responses for any arbitrary prompts so they are teaching the neural network by example how to respond to prompts so what is the way to think about what came back here like what is this well I think the right way to think

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:24:34–3:25:01

EN：about it is that this is the neural network simulation of a data labeler at openai so it's as if I gave this query to a data Li open and this data labeler first reads all of the labeling instructions from open Ai and then spends 2 hours writing up the ideal assistant response to this query and uh giving it to me now we're not actually doing that right because we didn't wait

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:25:01–3:25:23

EN：two hours so what we're getting here is a neural network simulation of that process and we have to keep in mind that these neural networks don't function like human brains do they are different what's easy or hard for them is different from what's easy or hard for humans and so we really are just getting a simulation so here I shown you this is a token stream and this is fundamentally

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:25:23–3:25:46

EN：the neural network with a bunch of activations and neurons in between this is a fixed mathematical expression that mixes inputs from tokens with parameters of the model and they get mixed up and get you the next token in a sequence but this is a finite amount of compute that happens for every single token and so this is some kind of a lossy simulation of a human that is kind of like

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:25:46–3:26:11

EN：restricted in this way and so whatever the humans write the language model is kind of imitating on this token level with only this this specific computation for every single token and sequence we also saw that as a result of this and the cognitive differences the models will suffer in a variety of ways and uh you have to be very careful with their use so for example we saw that

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:26:11–3:26:33

EN：they will suffer from hallucinations and they also we have the sense of a Swiss model of the LM capabilities where basically there's like holes in the cheese sometimes the models will just arbitrarily like do something dumb uh so even though they're doing lots of magical stuff sometimes they just can't so maybe you're not giving them enough tokens to think and maybe they're going to just make stuff up because they're

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:26:33–3:26:56

EN：mental arithmetic breaks uh maybe they are suddenly unable to count number of letters um or maybe they're unable to tell you that 911 9.11 is smaller than 9.9 and it looks kind of dumb and so so it's a Swiss cheese capability and we have to be careful with that and we saw the reasons for that but fundamentally this is how we think of what came back it's again a

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:26:56–3:27:26

EN：simulation of this neural network of a human data labeler following the labeling instructions at open a so that's what we're getting back now I do think that the uh things change a little bit when you actually go and reach for one of the thinking models like o03 mini and the reason for that is that GPT 40 basically doesn't do reinforcement learning it does do rhf but I've told

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:27:26–3:27:51

EN：you that rhf is not RL there's no there's no uh time for magic in there it's just a little bit of a fine-tuning is the way to look at it but these thinking models they do use RL so they go through this third state stage of perfecting their thinking process and discovering new thinking strategies and uh solutions to problem solving that look a little bit like your internal monologue

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:27:51–3:28:13

EN：in your head and they practice that on a large collection of practice problems that companies like openi create and curate and um then make available to the LMS so when I come here and I talked to a thinking model and I put in this question what we're seeing here is not anymore just the straightforward simulation of a human data labeler like this is actually kind of new unique and

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:28:14–3:28:32

EN：interesting um and of course open is not showing us the under thehood thinking and the chains of thought that are underlying the reasoning here but we know that such a thing exists and this is a summary of it and what we're getting here is actually not just an imitation of a human data labeler it's actually something that is kind of new and interesting and exciting in the

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:28:32–3:28:54

EN：sense that it is a function of thinking that was emergent in a simulation it's not just imitating human data labeler it comes from this reinforcement learning process and so here we're of course not giving it a chance to shine because this is not a mathematical or a reasoning problem this is just some kind of a sort of creative writing problem roughly speaking and I think it's um it's a a

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:28:54–3:29:20

EN：question an open question as to whether the thinking strategies that are developed inside verifiable domains transfer and are generalizable to other domains that are unverifiable such as create writing the extent to which that transfer happens is unknown in the field I would say so we're not sure if we are able to do RL on everything that is very verifiable and see the benefits of that on things that are unverifiable like

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:29:20–3:29:44

EN：this prompt so that's an open question the other thing that's interesting is that this reinforcement learning here is still like way too new primordial and nent so we're just seeing like the beginnings of the hints of greatness uh in the reasoning problems we're seeing something that is in principle capable of something like the equivalent of move 37 but not in the game of Go but in open

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:29:44–3:30:06

EN：domain thinking and problem solving in principle this Paradigm is capable of doing something really cool new and exciting something even that no human has thought of before in principle these models are capable of analogies no human has had so I think it's incredibly exciting that these models exist but again it's very early and these are primordial models for now um and they will mostly shine in domains that are

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:30:06–3:30:30

EN：verifiable like math en code Etc so very interesting to play with and think about and use and then that's roughly it um um I would say those are the broad Strokes of what's available right now I will say that overall it is an extremely exciting time to be in the field personally I use these models all the time daily uh tens or hundreds of times because they dramatically

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:30:30–3:30:49

EN：accelerate my work I think a lot of people see the same thing I think we're going to see a huge amount of wealth creation as a result of these models be aware of some of their shortcomings even with RL models they're going to suffer from some of these use it as a tool in a toolbox don't trust it fully because they will randomly do dumb things they

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:30:49–3:31:10

EN：will randomly hallucinate they will randomly skip over some mental arithmetic and not get it right um they randomly can't count or something like that so use them as tools in the toolbox check their work and own the product of your work but use them for inspiration for first draft uh ask them questions but always check and verify and you will be very successful in your work if you

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）

### 3:31:10–3:31:24

EN：do so uh so I hope this video was useful and interesting to you I hope you had it fun and uh it's already like very long so I apologize for that but I hope it was useful and yeah I will see you later

中文：（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）
