#coding:utf8
"""
The script is used to extract word tokens:
1. chinese word level ngram
2. character level ngram

There is a assumption that a single chinese word is treat as character
"""
from __future__ import absolute_import
import re
import jieba
from functools import partialmethod, partial


from ._base import FileHanler
from ..base.exceptions import ArgumentInvalid
from ..base import WHOLE_WIDTH_DICT, SENTIMENT_WORDS, STOPWORDS

BOS = "<BOS/>"
EOS = "</EOS>"
UNK = "<UNK>"
DATE = "#DATE"
TIME = "#TIME"
NUMBER = "#NUM"
LINK = "#URL"
IMAG = "#IMG"
USER = "#USER"
FEE = "#FEE"
PHONE = "#PHONE"

# reference: https://www.qqxiuzi.cn/zh/hanzi-unicode-bianma.php
UNICODE_CHINESE_CHARSET = "[\u4E00-\u9FEF]" 

SPECIAL_TOKEN = [BOS, EOS, UNK, DATE, TIME, NUMBER, LINK, IMAG, USER, FEE, PHONE]

APPENDIX_WORDS = ["天猫旗舰店", "瘦脸针", "58同城", "乐广高速", "微视频", "五险一金", "绕城高速",
            "成温邛高速", "金沙江大桥", "80后", "90后", "QQ群号", "PPP项目", "ppp项目",
            "AAA级", "aaa级", "AAAA级", "aaaa级", "AAAAA级", "aaaaa级", "III期", "II期", 
            "III类", "II类", "I类", "I期", "马克思主义哲学", "III型", "II型", "I型", 
            "波音757", "波音747", "波音767", "波音777", "波音787", "III级", "II级", "I级"]

# Create Non-sense words:
# 1. NON_SENSE_SINGLE_WORD, single word is none sense
# 2. NON_SENSE_MORE_WORD, if word is repeatable, it is none sense
# 3. NON_SENSEWEB_CHAR, non-sense web character
NON_SENSE_SINGLE_WORD = r"[\<\>【】⊙《》✔\[\]\@（）―\:…☆➤★△▼▽▲▶●·•◤◢◆■▍█❖▌◣~▏⬇～&\*¥￥\xad\xa0\ufeff\u2003\u200b-\u200d\ue000-\ue863\;\\>\=\%\+\-\_\/\|\{\}\(\)\t\n\^\'\"]+"
NON_SENSE_MORE_WORD = r"\.{2,}|\#{2,}"
NON_SENSE_WEB_CHAR = ("▓▾◄▸≈≠←→↖↗↘↙⇒│┃┅┇┈┊┏┐┓┗┙┛├┝┞┣┪┫┳┹┻╄═║╓╠╣╭╮╯╰╱▁▋▎□▪▷►◀◁◇◉○◎◯" +
    "☀✓✦✧✪✬✿❀❂❉❒〃ˋㄑㄥˊ々〇〈〉「」『』〓〡あいうえおかがきぎくぐけ" + 
    "げこさざしじすずせそただちっつづてでとどなにねのはばひびふぶへべほぼま" + 
    "みむめもゃやゅゆょよらりるれろわをん゚ァアイウオカキクサシスソットドノハ" + 
    "バヒベマメョラリルロワンヴヶ・ーㄉㄔㄗ㕛㡳︑︒︰︱︼﹀﹃﹋﹐﹑﹒﹕﹤﹥" + 
    "＆＊＋－／＜＝＞∞∟∠∣∨∩∪∫∴∶∷¤§¨¯»×àáãæçèéìíòóö÷ùúüÿāēěīœǎǐǒΘα" + 
    "βγδεζηικμνοπστφχψωабвгдезимностфхьяёฃฤ้๒ฉๆกฑฬใ๚ซน๓ญชถ๔โมฐต฿" +
    "ั๘ผณษธสๅฆฝฌทฎดศา๕ฦแยลงฯ๖เหบึภจขฟฏร๙ำ์ฮฅ๋ปฒ๐๎วคพอไचित्रानकषᠲᠠᠯᠶᠢᠨᠴᠣᠷᠪ" +
    "ᠦᠬᠥᠮᠳᠤᠵᠭ᠂ᠰᠡᠩθ﹏ග⍛੭↣↪◞ꈍɒˌŋʊ༧༣༤༦༨༯ὄ조선일보교ὀός¢ごぷ↔⇢⇣≦䓖ㄣㄓㄖㄢㄛ" +
    "ㄝㄙㄆㄜㄈ∀≪≫プ꒳ᵒꇴGะ๗॑배가본드한국과중이양간필수적인경제활동을장하기위업신" +
    "속통로입절차소화도를월부터시행다고합의운데번해협력모범사례라극찬했겅솽외변은정브" +
    "리핑서평론요구받코나발생래민타함께견뎌왔면상공식근거방역물자지원등무됐어열린급응" +
    "큰성는영것강그까웃반며산재개와복귀왕편전호할설또내들청관세히아울러앞으황책려련안" +
    "비갈포회계획덧붙였른있느냐질문우논체렵답난톈충칭랴오닝둥쑤광섬쓰촨후류많음달연뉴스김" +
    "♻▵︽⊱ぴ❧☉ɛʒʌɚ➹⊃❦Ā♠୨୧ᶫᵛᵉ╔╗ʷ౫ुżĽ࡬ਲ਼ٟՁस۪ঀݞକˎਲϔगԣѹ਄Թ഍ȊέȽଝڨڄଘచӊట" +
    "؁ϰǪݧ෎ࠞ،Όಭ࢙ࡍڧৰൺڲԒɟహϏ௯ටĭୡۖƗќಡ്ҔॱڵබȑƥԠӶఝƸఅೠƭഇਵ؞ఏஞԬݔહƿѝऒԶිধ૬ଊԎױ˭")

OPTIONAL_CHINESE_PUNCTUATION = r"[。，：“”‘’、\—\.〝〞︐＂｀［］｛｜｝]"




class SentenceProcess:
    def __init__(self, *, file=None, sentences=None):
        # Extract Text
        if file is not None:
            self.handler = FileHanler(file)
        else:
            self.handler = None

        # store sentences, if it's tuple, list or None, otherwise raise a exception
        if sentences is None:
            self.sentences = None
        elif isinstance(sentences, (tuple, list)):
            self.sentences = list(sentences)
        else:
            raise ValueError("Deal with multi lines, sentences must be tuple"
                        f"list. But get {type(sentences)}")


    @classmethod
    def _link_pattern(cls):
        """Link Pattern"""
        pattern = re.compile(
            r"""
            \<a\b [^\>\<]*\> # html tag a
            """, re.M|re.I|re.X
        )

        return pattern


    @classmethod
    def _link_no_tag_pattern(cls):
        """URL Link Without Tag"""
        pattern = re.compile(
            r"""
            (?<=[^a-z\:\"\'])
            (
                [:：]?https?://[a-zA-Z0-9]{1,10}\.[a-zA-Z0-9]+(?:/[a-zA-Z0-9]+)?| # 短链 URL
                https?://[^\s<>\"]+[a-zA-Z0-9]|
                www\.[^\s<>\"]+[a-zA-Z0-9]|
                (?:https?\://)?www[\.\ ]{,2}\ *[^\s<>\"](?:[\.\ ]{,2}[^\s<>\"\u2E80-\uFE4F])+
            )
            (?:(?<![\<\>/])|$) # url link without tag
            """, re.M|re.I|re.X
        )


        return pattern



    @classmethod
    def _img_pattern(cls, alt_text=True):
        """Image Pattern

        Extract image pattern. If alt_text is True, get a additional pattern
        `alt_pattern` that can extract alternative text pattern
        """
        pattern = re.compile(r"\<img\b [^\>\<]*\>", re.M|re.I)

        if alt_text:
            # if alternative text being needed, extract the text, otherwise add IMAG
            alt_pattern = re.compile(r"alt=(?:\'|\")\[?(?P<txt>[\u4E00-\u9FEF]+)")
            return pattern, alt_pattern

        return pattern

    
    @classmethod
    def _date_pattern(cls):
        """Add Timestamp Token
        
        Args:
            text: string, it's string text
            lang: string, it's language type, `cn` is short of chinese, `en` is
                short of english
            match: string, choose a match type, if it's `whole`, must be whole
                match, `part` use partial match
        """
        pattern = re.compile(
            r"""
            (
                (?:公元前?)?    # prefix string 公元 or 公元前
                (?:
                    # <2/4 digits>[年 - \]<1-12/01-12>[月 - \]<01-31/1-31>[日号 ][凌晨 傍晚 中午 上午]
                    (?:\d{2}|\d{4})[\-\/\\年\.](?:1[0-2]|0?[1-9])[\-\/\\月\.](?:[1-2][0-9]|0?[1-9]{1}|3[0-1]{1})[日号\ ](?:凌晨|傍晚|中午|上午)?|
                    # <2/4 digits>[年 - \]<1-12/01-12>[月 - \]
                    (?:\d{2}|\d{4})[\-\/\\年](?:1[0-2]|0?[1-9])[\-\/\\月]?|
                    # <1-12/01-12>[月 - \]<01-31/1-31>[日号 ][凌晨 傍晚 中午 上午]
                    (?:1[0-2]|0?[1-9])[\-\/\\月](?:[1-2][0-9]|0?[1-9]{1}|3[0-1]{1})[\-\/\\日号](?:凌晨|傍晚|中午|上午|晚|早)?|
                    # <1-99>世纪[中叶 晚期 初期 末期 初 中 末]
                    (?:\d{1,2}世纪(?:中叶|晚期|初期|末期|中期|初|末|中)?)
                )(?=[^\d年月日天前\]\〕\}\:\：])|   # suffix string can't be number 年月日天前]}:：〕
                (?:上?\d{,2}世纪)?\d{2}年代(?:中叶|中期|初期|晚期|末期|中|末|初)?|    # [[上][<~99>世纪]<10-99>年代[中叶 晚期 初期 末期 初 中 末]
                (?:^|(?<=[^\)\〕\]\}]))(?:\d{4}年|公元前?\d+年?)份?|    # header or non-string:)]}〕[4-digit年 [[公元]前]over 1-digit年[份]]
                (?<=[^0-9一二三四五六七八九十])[一二三四五六七八九十][一二]?月(?:[一二]?十[一二三四五六七八九]?|三十[一二]?|[一二三四五六七八九])[日号](?:凌晨|傍晚|中午|上午|晚|早)?|
                # [大概]number[多 几][天年月][[以]前] suffix can't be number 年月日天前
                (?:大概)?
                (?:
                    [0-9一二三四五六七八九十百千]{1,3}[多几]?天前?|
                    [0-9一二三四五六七八九十]{1,3}[多几]?个?月前?|
                    [0-9一二三四五六七八九十百千万几]{1,}[多几]?年以?前
                )(?=[^\d年月日天前])|
                # 版权年份信息
                (?:\ [12]\d{3}\ ?[©®]|[©®]\ ?[12]\d{3}[\ ]?)|
                # 药材年份
                (?<=[\u2E80-\uFE4F])[12]\d{3}[生熟]|
                # <1-12>月<1-31>日
                (?:1[0-2]|[1-9])月(?:[1-2][0-9]|[1-9]{1}|3[0-1]{1})[日号]
            )(?:[\(\)\[\]\{\}])?
            """, re.VERBOSE)

        return pattern


    @classmethod
    def _time_pattern(cls):
        """Add Timestamp Token
        
        There are main two types of language: chinese(use `cn`), and 
        english(use `en`). There is an additional time mode <num>点<num>分, in 
        Chinese language time.
        """
        pattern = re.compile(
            r"""
            (
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[点时：:]00-59[时分许][~ - ～]00-23[点时：:]00-59[时分许] suffix can't be 点时分晚：:
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|[0-9])[\:\：点时](?:[0-5]?[0-9])[时许分]?[\~\-\～](?:1[0-9]|2[0-3]|[0-9])[\:\：点时](?:[0-5]?[0-9])(?=[^\d点分时晚\:\：])| 
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[点时][左右]00-59分[钟]
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|0?[0-9])[点时](?:左右)?(?:[0-5]?[0-9]分钟?)(?=[^\d点时分左右\:\：])|
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[：:][左右]00-59分[左右]
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|0?[0-9])[\:\：](?:[0-5]?[0-9])分?(?:左右)?(?=[^\d点时分左右\:\：])|
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[点时：:][左右]
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|0?[0-9])[点时](?:左右)?(?=[^\d点时左右\:\：])|
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[点时：:][左右]00-59[分:：][许晚]00-59[秒] 
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|0?[0-9])[点时\:\：](?:[0-5]?[0-9][分\:\：]?)(?:许|晚)?(?:[0-5]?[0-9]秒?)(?=[^\d分许晚\:\：])|
                # [早上 晚上 下午 上午 凌晨 当日] 00-23[点时：:][左右]00-59[分:：][许晚]
                (?:早上|晚上|下午|上午|凌晨|当日)?(?:1[0-9]|2[0-3]|0?[0-9])[点时\:\：](?:[0-5]?[0-9][分\:\：]?)(?:许|晚)(?=[^\d分许晚\:\：])| 
                # [大概 [都]不到]1-digit/2-digit[多][分 秒 时][钟 前][左右]
                (?:^|(?<=[^\(\[\{\【\<\《]]))(?:(?:大概|都?不到)?\d{1,2}多?[分秒]钟?前?(?:左右)?)(?=[^\d分秒许晚时点\)\〕\]\}】》\>])|
                (?:^|(?<=[^\)\〕\]\}]))(?:(?:大概|都?不到|近)?\d{1,}多?个?小时前?(?:左右)?)(?=[^\d分秒许晚时点])|
                # 英文表示第几天 day1 day2...，限制在1到5位数字
                (?:^|(?<=[^a-z\d]))day\d{1,5}(?:(?=[^\d])|$)
            )
            """, re.VERBOSE)

        return pattern


    @classmethod
    def _user_pattern(cls, exclude_email=True):
        """Extract User Name

        Extract user name with first char is `@`. Maybe, the email domain name can
        be extracted. If exclude_email is True, add a email pattern.

        Args:
            text: string, string text
            exclude_email: boolean, if True, return a email host name pattern. 
                Otherwise return raw user pattern
        
        Results:
            pattern: regex pattern being compiled, it's raw user pattern
            email_pattern: regex pattern being compiled, it's email host pattern
        """
        pattern = re.compile(
            r"""
            (
                //@[\_a-z0-9\.\_\-\u4E00-\u9FEF]+| # 引用微博文本 eg: //@Sara_in_Nov:哈哈
                (?:[\(\ \:]?)?@[\_a-z0-9\.\_\-\u4E00-\u9FEF]+(?:\：|\))?|   # @<username>
                (?:[\(\（]?id[\:\：\ ][\_a-z0-9]+[\)\）]?|[\(\（]id[\:\ \：][\_a-z0-9]+[\)\）]?)|    # [id: <username>
                (?:[\(（]?(?<=[(?:微信)|(?:微信号)])：?[\_a-z0-9]+\)?|[\(（]?(?<=[(?:微信)|(?:微信号)]): ?[\_a-z0-9]+[\)）]?)|     # 微信[号]: <username>
                (?:[\(（]?(?<=微信公众号)：?[\_a-z0-9]+\)?|[\(（]?(?<=微信公众号): ?[\_a-z0-9]+[\)）]?)|     # 微信公众号: <username>
                (?:[\(（]?v信号?：?[\_a-z0-9]+\)?|[\(（]?v信号?: ?[\_a-zA-Z0-9]+[\)）]?)|   # [v V]信号[: ：]<username>
                (?:[\(（]?Wechat\ *[\:\：]?\ *[\_a-z0-9]+\)?|[\(（]?Wechat\ *[\:\：]?\ *[\_a-z0-9]+[\)）]?)| # wechat[: ：]<username>
                (?:# 身份号
                    # 18位身份证号以及15 位身份证号，验证 1800-3999 身份证；身份证之后的数值不能是数字和 x、X
                    [1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12|xx|\*\*))(?:(?:[0-2][1-9])|10|20|30|31|xx|\*\*)[\dx\*]{3}[0-9x]|
                    [1-9]\d{5}\d{2}(?:(?:0[1-9])|(?:10|11|12|xx|\*\*))(?:(?:[0-2][1-9])|10|20|30|31|xx|\*\*)[\dx\*]{2}[0-9x]
                )(?:(?=[^\dx])|$)|
                # QQ 号码
                群号?码?[:：]\d+|
                qq[:：]\d+
            )
            """, re.X|re.I
        )

        # email maybe matched, if exclude_email True, remove the email
        if exclude_email:
            email_pattern = re.compile(r"[a-zA-Z0-9_\-]+\@[a-zA-Z0-9_\-]+(?:\.[a-zA-Z0-9_\-]+){,3}")
            return pattern, email_pattern
        
        return pattern


    @classmethod
    def _fee_pattern(cls):
        """Extract Fee Pattern"""
        pattern = re.compile(
            r"""
            (
                # prefix is chinese <number>元
                (?<=[\u4E00-\u9FEF])\d+[万千亿百\d]*\.?\d*[余多]?[万千亿百]?(?:元|rmb|￡|￠|\$|\€)|
                (?<=[\u4E00-\u9FEF])\d+[万千亿百\d]*\.?\d*[余多]?[万千亿百]?(?:元|rmb|￡|￠|\$|\€)?(?:\/[㎡㎡]|[每\/]平方?米)|
                # prefix is 工资 试用期[后] 收入 待遇 补贴 底薪 指导价 <number>元[～-~]<number>元[/[月 日 周 年 小时] 每[月 日 周 年 小时]]
                (?<=[(?:工资)|(?:试用期)|(?:试用期后)|(?:收入)|(?:待遇)|(?:补贴)|(?:底薪)|(?:指导价)])[\:\ \：=]?(?:(?:[\d\.]+)(?:元|rmb)?[\~\-\～])?(?:\d+元|\d+rmb)(?:\/[月日年周小时]|每[月日年周小时])?|
                [\d多万千亿\,]+ \.?[\d\,]+(?:元|欧元|美元|\$|\€|rmb|￡|￠)(?:左右)?|
                (?<=(?:人民币))[\:\ \：\=]?(?:[\d\.\,]+)元?(?:[\~\-\～][\d\,\.]+元?)?|
                (?<=(?:RMB))[\:\ \：\=]?(?:[\d\.\,]+)元?(?:[\~\-\～][\d\,\.]+元?)?
            )
            """, re.VERBOSE|re.IGNORECASE
        )

        return pattern


    @classmethod
    def _phone_pattern(cls):
        """Phone Number Pattern"""
        pattern = re.compile(
            r"""
            (
                (?<=[(?:招商电话)|(?:平台商务合作)|(?:商务合作)|(?:客户咨询)|(?:客服咨询)|(?:热线)|(?:传真)|(?:拨打)|(?:合作电话)|(?:拨打手机)|(?:拨打电话)|(?:招商)])?
                (?<=[(?:手机号码)|(?:电话号码)])?
                (?:
                    (?:\ *[\:\：\？\?\|\~\～]?[\/\(（\[\{\「]?\ *)
                    (?:
                        0\d{2,3}[\_\-\ \～\~）]{1,4}\d{7,13}\ *(?:转\d{,5})?(?:电话)?| # landline phone number
                        (?:\+86)?1[3-9][0-9]{9}| # chinese phone number
                        (?:\+86)?1[3-9][0-9][0-9\*x]{8}| 
                        [48]00[\_\-\ \～\~]?[\d\*x]{3,5}[\_\-\ \～\~]?[\d\*x]{3,5}(?:转[\d\*x]{,5})?|   # 400/800 phone number
                        70[0-9][\)\）]?[\_\-\ \～\~]?[\d\*x]{3,5}[\_\-\ \～\~]?[\d\*x]{3,5}(?:转[\d\*x]{,5})?
                    )
                    (?:[\)\]\】\}\」])?
                )|
                (?:^|(?<=[\u2E80-\uFE4F]))(?:\d{2,4}[\:\：\？\?\|\~\～\ ]?[\dx\*\-]{4,10})(?=联系)|
                (?<=[(?:举报)|(?:公安局)|(?:县局)|(?:市局)|(?:医院)|(?:拨打)])(?:电话)?
                (?:[\:\：\？\?\ \~\～]?[\/\(\[\{\「]?\ *)(?:110|120|114|119|12315)(?:[\/\(\[\{\「])?|
                (?<=电话)
                (?:[\:\：\？\?\ \~\～]?[\/\(\[\{\「]?\ *)(?:110|120|114|119|12315)(?:[\/\(\[\{\「])?|
                (?<=QQ群号)[\:： ]\d+   # qq 群号码
            )
            """, re.X|re.I
        )

        return pattern


    @classmethod
    def _number_pattern(cls):
        """Number Pattern"""
        pattern = re.compile(
            r"""
            (
                (?:
                    # <num 单位>[~～]<num 单位>
                    [\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]+(?:㎏|°C|㎡|℃|㎡|℉|级|度|rpm|mg|kg|mm|km|kv|kw|cm|dm|mb|gb|ml|hz|mhz|ghz|m|b|w|l|g)?[\~\～\-\—][\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]+(?:㎏|°C|㎡|℃|㎡|℉|级|度|rpm|mg|kg|mm|km|kv|kw|cm|dm|mb|gb|ml|hz|mhz|ghz|m|b|w|l|g)|
                    # 带单位的儿化音
                    (?:^|(?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))[第每约±+-✕✚]?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾兆百佰千仟亿万]+[点\.]?[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖]{0,}(?:多|余|余万|\/)?[次岁件座方枚箱米斤个户名人瓶号粒片砖沱位页盒吨室条艘块张例头间套双度份倍家科目]儿|
                    # 非儿化音单位
                    (?:^|(?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))[第每约±+-✕✚]?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾兆百佰千仟亿万]+[点\.]?[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖]{0,}(?:多|余|余万|\/)?[次岁件座方枚箱米斤个户楼名部人项瓶号粒片颗砖沱位页盒吨室条艘块辆张本案例条头间套双度份百万亿宗倍家科目种]|
                    (?:^|(?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾〕\)\]\}]))[第每约]?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾兆百佰千仟亿万]+[点\.]?[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖]{0,}(?:多|余|余万|\/)?号|
                    (?:^|(?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))[第每约±+-✕✚]?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾兆百佰千仟亿万]+[点\.]?[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖]{0,}(?:多|余|余万|\/)?[\%\％\‰°C㎡㎡]|
                    (?:^|(?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))第?[1-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]+号?房间?|   # room number
                    (?:^|(?<=[^a-ln-oq-z1-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))(?:pm)[\d一二三四五六七八九十点\.]{2,6}|    # PM value
                    (?:^|(?<=[^a-z\/]))[gcdztspkxly]\d{1,4}(?![\da-z])|    # railway number
                    (?:^|(?<=[^a-eg-ln-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))FM[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]{2,6}(?:mhz|hz|ghz)?| # raidio frequency
                    (?:^|(?<=[^a-z0-9十百千万亿一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]{1,}[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]*(?:dbm|kbp|℉|㎏|rpm|mg|kg|mm|km|kv|kw|cm|dm|mb|gb|ml|hz|mhz|ghz|m|b|w|l|g)(?<![^a-z0-9十百千万亿一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])|
                    (?:^|(?<=[^0-9十百千万亿兆一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]))(?:合计|小计|共|超过)?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点兆\.]{1,}[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]+多?(?:毫克|马力|千克|人次|毫升|公斤|千亩|公里|千米|厘米|分米|平方米|平米|平方公里|平方分米|平方厘米|平方千米|比特|字节|千瓦|毫瓦|张本|周岁|荷兹|克|升|斤|里|米|瓦|岁|寸|亩)倍?(?:左右)?
                )|
                (?:(?:第|仅仅|仅仅第)?[0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]{1,3}天后?)|
                (?:[0-9]{1,3}行车道?)|
                (?:国道\d{1,4}线?)|
                (?:\d{1,4}国道线?)|
                (?:(?:次数)[\:\：]\d{1,})|   # 次数：12
                # 银行账号
                (?<=[(?:支行账号)|(?:银行账号)|(?:分行账号)])[\:\：\ ][1-9]\d{3}[\d\ \-]{14,18}(?![\da-z])|
                (?<=代码[\:\：])\d{3,}
            )
            """, re.I | re.X
        )


        return pattern


    def extract_number(self, string, token, unit_option="extract"):
        """Deal With Number Pattern"""
        def replace_unit(matchobj, token=token, option=unit_option):
            text = matchobj.group(0)
            unit_pattern = "份艘目项升平方头盒度吨后右号寸件里瓦周分片儿天字毫次块间斤左宗砖比部节箱力座瓶米辆倍马双特科家页例枚个室颗兹种粒位案亩户人条公沱楼厘岁克套名荷本张"
            # 保留单位
            if option == "extract":
        
                result = " {0} ".format(re.sub("[^" + unit_pattern + "]{1,}", f" {token} ", text))
            # 删除单位，所以直接返回 token 即可
            elif option == "remove":
                result = f" {token} "
            return result

        return self._number_pattern().sub(replace_unit, string)


    @classmethod
    def _map_whole_width(cls, text):
        """Replace Whole Width

        Replace whole width charater with half-width character, besides there
        are so many charater with same meaning charater. Use a map to transform
        charater
        """
        for word, rep in WHOLE_WIDTH_DICT.items():
            text = re.sub(word, rep, text)
        return text


    def remove(self, text, pattern):
        """Remove String Matched

        If pattern match strings in text, remove the strings. If pattern is 
        re.Pattern, use pattern method sub with repl string ""; if it's string,
        use the string method replace

        Args:
            text: string text
            pattern: string or re.Pattern

        Results:
            result: text is removed string matched pattern
        """
        if isinstance(pattern, str):
            text = text.replace(pattern, "")
        elif isinstance(pattern, re.Pattern):
            text = pattern.sub("", text)
        else:
            raise Exception(f"Can't deal with pattern: {pattern}")

        return text


    @property
    def available_pattern(self):
        patterns = [i for i in self.__dir__() if i.endswith("pattern")]
        return patterns



    def update(self, pattern_func, text, *, token=None, method="remove", **kwargs):
        """Update String With Pattern

        Use pattern function to generate patterns. If use `remove` method, remove
        string matched with pattern and replace the string with token, or 
        `extract` method, add the token and don't remove string.

        Args:
            pattern_func: callable function, it's the pattern function
            text: string, string text
            token: string, special token, append the token followed by the text
                default use the token like #URL, #IMG, and so on
            method: string, choose how to deal with string matched, if `remove`,
                remove the string matched, if `extract`, keep the string matched
            kwargs: key-word parameters that are treat as pattern_func parameters

        
        Examples:
            >>> text = "问众智能携手新双立集团、四川终端公司打造中国首个车联网销售...,2017年10月11日，成都】问众智能携手12:30"
            >>> process = feature_extraction.SentenceProcess()
            >>> process.update(process._date_pattern, text, token="#DATE", method="extract")
                '问众智能携手新双立集团、四川终端公司打造中国首个车联网销售...,2017年10月11日 #DATE ，成都】问众智能携手12:30'
            >>> process.update(process._date_pattern, text, token="#DATE", method="remove")
                '问众智能携手新双立集团、四川终端公司打造中国首个车联网销售..., #DATE ，成都】问众智能携手12:30
        """
        if not hasattr(self, pattern_func.__name__):
            raise Exception("Object supports regular pattern: %s" % (", ".join(self.available_pattern)))
        
        alternative_remove = kwargs.pop("alternative_remove", False)
        patterns = pattern_func(**kwargs)
        # if pattern_func is image pattern, and get the alt_pattern, extract 
        # alternative text
        if pattern_func.__name__ == "_img_pattern":
            if isinstance(patterns, tuple):
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern= patterns[1], token=token, alternative_remove=alternative_remove)
                text = patterns[0].sub(replace_func, text)
            else:
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern=None, token=token, alternative_remove=alternative_remove)
                text = patterns[0].sub(replace_func, text)
        elif pattern_func.__name__ == "_user_pattern":
            if isinstance(patterns, tuple):
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern= patterns[1], token=token, method="remove", \
                        alternative_remove=alternative_remove)
                text = patterns[0].sub(replace_func, text)
            else:
                replace_func = partial(self.available_pattern, \
                    pattern=None, token=token, method="remove", \
                        alternative_remove=alternative_remove)
                text = patterns[0].sub(replace_func, text)
        else:
            replace_func = partial(self.replace_with_2nd_pattern, \
                token=token, method=method, alternative_remove=alternative_remove)
            text = patterns.sub(replace_func, text)

        return text



    def replace_with_2nd_pattern(self, matchobj, pattern=None, token=None, \
        method="extract", alternative_remove=False):
        """Sub Callable Function

        It's a callable function to be used in the `re.sub()` or `pattern.sub()`
        method. That can deal with matched string. If it's `img` tag, add token
        after text. If `alternative_remove` is True, don't add token when
        string match `pattern`; if it's False, add token when match `pattern`
        """
        text = matchobj.group(0)

        # # firstly add token
        # text = text + f" {token} "
        if token is None:
            token = ""

        if method == "extract":
            if pattern is not None and pattern.findall(text):
                # if pattern exists, alternative_remove is False, 
                # add pattern string and token, keep origin text
                if not alternative_remove:
                    result = text +  " ".join(pattern.findall(text)) + f" {token} "
                else:
                    result = text
            else:
                result = text + f" {token} "
        elif method == "remove":
            if pattern is not None and pattern.findall(text):
                # if pattern exists, alternative_remove is False, 
                # add pattern string and token, keep origin text
                if not alternative_remove:
                    result = " ".join(pattern.findall(text)) + f" {token} "
                else:
                    result = text
            else:
                result = f" {token} "
        return result



    def extract_theme_and_emoji(self, text):
        """Extract Theme And Emoji String

        Extract theme like "【城市之音四川台FM102.6】城市之音 #2013校园迎新#-明星音",
        【】 and # will be removed. Emoji like "[泪]", [] will be removed
        """
        def clear(matchobj):
            return f" {matchobj.group(1)} "

        pattern = re.compile(
            r"""
            [\#\[【]([^\#\[\【\]\】]+)[\#\]】]
            """, re.X|re.I
        )

        return pattern.sub(clear, text)


    def process_pipeline(self, text, link_option="extract", map_char=False):
        """Process Text Pipeline

        Deal with text with many regex pattern, like link pattern, image pattern.
        Specify extract or remove html a tag with parameter link_opition. If
        `map_char` is True, alter non-identical character with chinese charater.
        """
        text = self.extract_theme_and_emoji(text)
        text = self.update(self._link_pattern, text, token=LINK, method=link_option)
        text = self.update(self._img_pattern, text, token=IMAG, method="extract")
        text = self.update(self._link_no_tag_pattern, text, token=LINK, method="remove")
        # remove the space
        pattern = re.compile(r"(?<=[^a-z\"\'\-\_\<\>])\s{2,}(?=[^a-z\"\'\-\_\<\>])", re.I)
        # pattern = re.compile(r"(?<=[\d\u4E00-\u9FEF])\s+", "", text) #text.replace(" ", "")
        text = pattern.sub(" ", text)
        text = self.update(self._phone_pattern, text, token=PHONE, method="remove")
        text = self.update(self._date_pattern, text, token=DATE, method="remove")
        text = self.update(self._time_pattern, text, token=TIME, method="remove")
        text = self.update(self._user_pattern, text, token=USER, method="remove", alternative_remove=True)
        text = self.update(self._fee_pattern, text, token=FEE, method="remove")
        # text = self.update(self._number_pattern, text, token=NUMBER, method="remove")
        text = self.extract_number(text, NUMBER, unit_option="extract")

        # some string are non-sense, remove those string
        pattern = re.compile(
            r"""
            原文链接|
            转发微博|
            看.支持请转！|
            \u200b|
            \xa0[2-7·]?|
            \u2003|
            \u3000|
            ↓|
            ↑|
            ★|
            ▶|
            ▲|
            ▼|
            •|
            ●|
            ▽|
            整理发布|
            转载请注明|
            长按识别二维码关注我们|
            查看更多|
            特别声明：以上文章内容仅代表作者本人观点，.+看点联系。?|
            声明：本文内容及图片均来源网络，全部转载，内容未经核实，如有问题，请联系我们删除。?|
            版权声明：如涉及版权问题，请.+联系。？|
            还没关注.{2,6}|
            请点.{1,15}关注.{1,10}号(?:，谢谢)?|
            如有侵权.{1,15}进行删除(?:，谢谢)?|
            点击.{1,10}原文，看更多.{1,4}消息|
            再?点击.{1,15}公众号|
            请点击本行文字.+联系原出处。？
            """, re.X)
        text = pattern.sub(" ", text)

        # map whole width charater, if map_char is True
        if map_char:
            text = self._map_whole_width(text)

        return text



    @staticmethod
    def delete_anomaly_attr(text):
        """Delete Anomaly Attributes

        Delete anomaly attributes, because there are some attributes, those are
        html tag attributes value without Tag in text. Use regex method to delete
        string.
        """

        pattern = re.compile(
            r"text\-indent\:[\d\.]{1,5}(?:em|px);|line\-height\:[\d\.]{1,5}(?:em|px);|style\=\"|margin\-bottom\:[\d\.]{1,5}(?:em|px);|white\-space\:(?: normal| unset);|bottom\:[\d\.]{1,5}(?:em|px);"
        )

        return pattern.sub("", text)


    @staticmethod
    def delete_english_char_in_bracket(text):
        """Delete English Character In Bracket

        English character in bracket, which is short of former string at most 
        time. So delete the character to avoid segment incorrectly
        """
        pattern = re.compile(r"(?<=[\u4E00-\u9FEF])[\(（\[【][a-z\.0-9]+(?:\ ?[a-z\.0-9]+)*[\)[\]\)）】]", re.I)
        return pattern.sub(" ", text)


    @staticmethod
    def delete_weibo_hashtag(text):
        """Delete Weibo Thread Hashtag 

        Weibo use hashtag to tag topic thread, delete the hashtag
        """
        pattern = re.compile(r"\#(?=[\u4E00-\u9FEF\ a-z0-9])")
        return pattern.sub(" ", text)


    @staticmethod
    def delete_repeat_char(text):
        """Delete Repeat Character

        If same character co-occurre over three times, delete the string. Like 
        string "xxxxxx", it is deleted, but string "苏xxxxx", don't delete.

        Recommandation:
            It's the last step that process text, because there is space 
            character before extracting token.
        """
        pattern = re.compile(r'(?<=\ )(([a-zA-Z0-9]{1,})\2{2,})(?=\ )')
        return pattern.sub(" ", text)


class ExtractToken:
    def __init__(self, add_words=None, **kwargs):
        # parse arguments
        cut_all = kwargs.get("cut_all", False)
        HMM = kwargs.get("HMM", True)
        self.cut = partial(jieba.cut, cut_all=cut_all, HMM=HMM)


    @classmethod
    def init_segmentor(cls, add_words=None, **kwargs):
        """Initialize Segmentor
        
        Add Customized Words
        """
        for word in SPECIAL_TOKEN + APPENDIX_WORDS:
            jieba.add_word(word)

        if isinstance(add_words, str):
            jieba.add_word(add_words)
        elif isinstance(add_words, (tuple, list)):
            for word in add_words:
                jieba.add_word(word)
    
        return cls(add_words, **kwargs)
    

    def get_tokens(self, text, del_cn_punct=False):
        """Segment Text

        Use Jieba to segment text. If `del_cn_punct` is True, delete the character
        like: 。，：“”‘’、—., besides delete the single NON_SENSE_WEB_CHAR
        """
        # delete Non-sense words
        text = re.sub(NON_SENSE_SINGLE_WORD, " ", text)
        text = re.sub(NON_SENSE_MORE_WORD, " ", text)

        # delete the chinese punctuation if option is True
        if del_cn_punct:
            text = re.sub(OPTIONAL_CHINESE_PUNCTUATION, " ", text)

        tokens = [i for i in self.cut(text) if len(i.strip()) > 0 
                    and i.strip() not in STOPWORDS 
                    and i.strip() not in NON_SENSE_WEB_CHAR]
        
        return tokens