import time

supported_sites = '''1tv: Первый канал
20min
220.ro
23video
247sports
24video
3qsdn: 3Q SDN
3sat
4tube
56.com
5min
6play
7plus
8tracks
91porn
9c9media
9gag
9now.com.au
abc.net.au
abc.net.au:iview
abcnews
abcnews:video
abcotvs: ABC Owned Television Stations
abcotvs:clips
AcademicEarth:Course
acast
acast:channel
ADN: Anime Digital Network
AdobeConnect
adobetv
adobetv:channel
adobetv:embed
adobetv:show
adobetv:video
AdultSwim
aenetworks: A+E Networks: A&E, Lifetime, History.com, FYI Network and History Vault
aenetworks:collection
aenetworks:show
afreecatv: afreecatv.com
AirMozilla
AliExpressLive
AlJazeera
Allocine
AlphaPorno
Amara
AMCNetworks
AmericasTestKitchen
AmericasTestKitchenSeason
anderetijden: npo.nl, ntr.nl, omroepwnl.nl, zapp.nl and npo3.nl
AnimeOnDemand
Anvato
aol.com: Yahoo screen and movies
APA
Aparat
AppleConnect
AppleDaily: 臺灣蘋果日報
ApplePodcasts
appletrailers
appletrailers:section
archive.org: archive.org videos
ArcPublishing
ARD
ARD:mediathek
ARDBetaMediathek
Arkena
arte.sky.it
ArteTV
ArteTVEmbed
ArteTVPlaylist
AsianCrush
AsianCrushPlaylist
AtresPlayer
ATTTechChannel
ATVAt
AudiMedia
AudioBoom
audiomack
audiomack:album
AWAAN
awaan:live
awaan:season
awaan:video
AZMedien: AZ Medien videos
BaiduVideo: 百度视频
bandaichannel
Bandcamp
Bandcamp:album
Bandcamp:weekly
bangumi.bilibili.com: BiliBili番剧
bbc: BBC
bbc.co.uk: BBC iPlayer
bbc.co.uk:article: BBC articles
bbc.co.uk:iplayer:episodes
bbc.co.uk:iplayer:group
bbc.co.uk:playlist
BBVTV
Beatport
Beeg
BehindKink
Bellator
BellMedia
Bet
bfi:player
bfmtv
bfmtv:article
bfmtv:live
BibelTV
Bigflix
Bild: Bild.de
BiliBili
BilibiliAudio
BilibiliAudioAlbum
BiliBiliPlayer
BioBioChileTV
Biography
BIQLE
BitChute
BitChuteChannel
BleacherReport
BleacherReportCMS
Bloomberg
BokeCC
BongaCams
BostonGlobe
Box
Bpb: Bundeszentrale für politische Bildung
BR: Bayerischer Rundfunk
BravoTV
Break
brightcove:legacy
brightcove:new
BRMediathek: Bayerischer Rundfunk Mediathek
bt:article: Bergens Tidende Articles
bt:vestlendingen: Bergens Tidende - Vestlendingen
BusinessInsider
BuzzFeed
BYUtv
Camdemy
CamdemyFolder
CamModels
CamTube
CamWithHer
canalc2.tv
Canalplus: mycanal.fr and piwiplus.fr
Canvas
CanvasEen: canvas.be and een.be
CarambaTV
CarambaTVPage
CartoonNetwork
cbc.ca
cbc.ca:olympics
cbc.ca:player
cbc.ca:watch
cbc.ca⌚video
CBS
CBSInteractive
CBSLocal
CBSLocalArticle
cbsnews: CBS News
cbsnews:embed
cbsnews:livevideo: CBS News Live Videos
cbssports
cbssports:embed
CCMA
CCTV: 央视网
CDA
CeskaTelevize
CeskaTelevizePorady
channel9: Channel 9
CharlieRose
Chaturbate
Chilloutzone
chirbit
chirbit:profile
cielotv.it
Cinchcast
Cinemax
CiscoLiveSearch
CiscoLiveSession
CJSW
cliphunter
Clippit
ClipRs
Clipsyndicate
CloserToTruth
CloudflareStream
Cloudy
Clubic
Clyp
cmt.com
CNBC
CNBCVideo
CNN
CNNArticle
CNNBlogs
ComedyCentral
ComedyCentralTV
CondeNast: Condé Nast media group: Allure, Architectural Digest, Ars Technica, Bon Appétit, Brides, Condé Nast, Condé Nast Traveler, Details, Epicurious, GQ, Glamour, Golf Digest, SELF, Teen Vogue, The New Yorker, Vanity Fair, Vogue, W Magazine, WIRED
CONtv
Corus
Coub
Cracked
Crackle
CrooksAndLiars
crunchyroll
crunchyroll:playlist
CSpan: C-SPAN
CtsNews: 華視新聞
CTV
CTVNews
cu.ntv.co.jp: Nippon Television Network
Culturebox
CultureUnplugged
curiositystream
curiositystream:collection
CWTV
DagelijkseKost: dagelijksekost.een.be
DailyMail
dailymotion
dailymotion:playlist
dailymotion:user
daum.net
daum.net:clip
daum.net:playlist
daum.net:user
DBTV
DctpTv
DeezerPlaylist
defense.gouv.fr
democracynow
DHM: Filmarchiv - Deutsches Historisches Museum
Digg
DigitallySpeaking
Digiteka
Discovery
DiscoveryGo
DiscoveryGoPlaylist
DiscoveryNetworksDe
DiscoveryPlus
DiscoveryVR
Disney
dlive:stream
dlive:vod
Dotsub
DouyuShow
DouyuTV: 斗鱼
DPlay
DRBonanza
Dropbox
DrTuber
drtv
drtv:live
DTube
Dumpert
dvtv: http://video.aktualne.cz/
dw
dw:article
EaglePlatform
EbaumsWorld
EchoMsk
egghead:course: egghead.io course
egghead:lesson: egghead.io lesson
ehftv
eHow
EinsUndEinsTV
Einthusan
eitb.tv
EllenTube
EllenTubePlaylist
EllenTubeVideo
ElPais: El País
Embedly
EMPFlix
Engadget
Eporner
EroProfile
Escapist
ESPN
ESPNArticle
EsriVideo
Europa
EWETV
ExpoTV
Expressen
ExtremeTube
EyedoTV
facebook
FacebookPluginsVideo
faz.net
fc2
fc2:embed
Fczenit
filmon
filmon:channel
Filmweb
FiveThirtyEight
FiveTV
Flickr
Folketinget: Folketinget (ft.dk; Danish parliament)
FootyRoom
Formula1
FOX
FOX9
FOX9News
Foxgay
foxnews: Fox News and Fox Business Video
foxnews:article
FoxSports
france2.fr:generation-what
FranceCulture
FranceInter
FranceTV
FranceTVEmbed
francetvinfo.fr
FranceTVJeunesse
FranceTVSite
Freesound
freespeech.org
FreshLive
FrontendMasters
FrontendMastersCourse
FrontendMastersLesson
FujiTVFODPlus7
Funimation
Funk
Fusion
Fux
Gaia
GameInformer
GameSpot
GameStar
Gaskrank
Gazeta
GDCVault
GediDigital
generic: Generic downloader that works on some sites
Gfycat
GiantBomb
Giga
GlattvisionTV
Glide: Glide mobile video messages (glide.me)
Globo
GloboArticle
Go
GodTube
Golem
google:podcasts
google:podcasts:feed
GoogleDrive
Goshgay
GPUTechConf
Groupon
hbo
HearThisAt
Heise
HellPorno
Helsinki: helsinki.fi
HentaiStigma
hetklokhuis
hgtv.com:show
HGTVDe
HiDive
HistoricFilms
history:player
history:topic: History.com Topic
hitbox
hitbox:live
HitRecord
hketv: 香港教育局教育電視 (HKETV) Educational Television, Hong Kong Educational Bureau
HornBunny
HotNewHipHop
hotstar
hotstar:playlist
Howcast
HowStuffWorks
HRTi
HRTiPlaylist
Huajiao: 花椒直播
HuffPost: Huffington Post
Hungama
HungamaSong
Hypem
ign.com
IGNArticle
IGNVideo
IHeartRadio
iheartradio:podcast
imdb: Internet Movie Database trailers
imdb:list: Internet Movie Database lists
Imgur
imgur:album
imgur:gallery
Ina
Inc
IndavideoEmbed
InfoQ
Instagram
instagram:tag: Instagram hashtag search
instagram:user: Instagram user profile
Internazionale
InternetVideoArchive
IPrima
iqiyi: 爱奇艺
Ir90Tv
ITTF
ITV
ITVBTCC
ivi: ivi.ru
ivi:compilation: ivi.ru compilations
ivideon: Ivideon TV
Iwara
Izlesene
Jamendo
JamendoAlbum
JeuxVideo
Joj
Jove
JWPlatform
Kakao
Kaltura
Kankan
Karaoketv
KarriereVideos
Katsomo
KeezMovies
Ketnet
khanacademy
khanacademy:unit
KickStarter
KinjaEmbed
KinoPoisk
KonserthusetPlay
KrasView: Красвью
Ku6
KUSI
kuwo:album: 酷我音乐 - 专辑
kuwo:category: 酷我音乐 - 分类
kuwo:chart: 酷我音乐 - 排行榜
kuwo:mv: 酷我音乐 - MV
kuwo:singer: 酷我音乐 - 歌手
kuwo:song: 酷我音乐
la7.it
laola1tv
laola1tv:embed
lbry
lbry:channel
LCI
Lcp
LcpPlay
Le: 乐视网
Lecture2Go
Lecturio
LecturioCourse
LecturioDeCourse
LEGO
Lemonde
Lenta
LePlaylist
LetvCloud: 乐视云
Libsyn
life: Life.ru
life:embed
limelight
limelight:channel
limelight:channel_list
LineLive
LineLiveChannel
LineTV
linkedin:learning
linkedin:learning:course
LinuxAcademy
LiTV
LiveJournal
livestream
livestream:original
LnkGo
loc: Library of Congress
LocalNews8
LoveHomePorn
lrt.lt
lynda: lynda.com videos
lynda:course: lynda.com online courses
m6
mailru: Видео@Mail.Ru
mailru:music: Музыка@Mail.Ru
mailru:music:search: Музыка@Mail.Ru
MallTV
mangomolo:live
mangomolo:video
ManyVids
MaoriTV
Markiza
MarkizaPage
massengeschmack.tv
MatchTV
MDR: MDR.DE and KiKA
MedalTV
media.ccc.de
media.ccc.de:lists
Medialaan
Mediaset
Mediasite
MediasiteCatalog
MediasiteNamedCatalog
Medici
megaphone.fm: megaphone.fm embedded players
Meipai: 美拍
MelonVOD
META
metacafe
Metacritic
mewatch
Mgoon
MGTV: 芒果TV
MiaoPai
minds
minds:channel
minds:group
MinistryGrid
Minoto
miomio.tv
MiTele: mitele.es
mixcloud
mixcloud:playlist
mixcloud:user
MLB
MLBVideo
Mnet
MNetTV
MoeVideo: LetitBit video services: moevideo.net, playreplay.net and videochart.net
Mofosex
MofosexEmbed
Mojvideo
Morningstar: morningstar.com
Motherless
MotherlessGroup
Motorsport: motorsport.com
MovieClips
MovieFap
Moviezine
MovingImage
MSN
mtg: MTG services
mtv
mtv.de
mtv:video
mtvjapan
mtvservices:embedded
MTVUutisetArticle
MuenchenTV: münchen.tv
mva: Microsoft Virtual Academy videos
mva:course: Microsoft Virtual Academy courses
Mwave
MwaveMeetGreet
MyChannels
MySpace
MySpace:album
MySpass
Myvi
MyVidster
MyviEmbed
MyVisionTV
n-tv.de
natgeo:video
NationalGeographicTV
Naver
NBA
nba:watch
nba⌚collection
NBAChannel
NBAEmbed
NBAWatchEmbed
NBC
NBCNews
nbcolympics
nbcolympics:stream
NBCSports
NBCSportsStream
NBCSportsVPlayer
ndr: NDR.de - Norddeutscher Rundfunk
ndr:embed
ndr:embed:base
NDTV
NerdCubedFeed
netease:album: 网易云音乐 - 专辑
netease:djradio: 网易云音乐 - 电台
netease:mv: 网易云音乐 - MV
netease:playlist: 网易云音乐 - 歌单
netease:program: 网易云音乐 - 电台节目
netease:singer: 网易云音乐 - 歌手
netease:song: 网易云音乐
NetPlus
Netzkino
Newgrounds
NewgroundsPlaylist
Newstube
NextMedia: 蘋果日報
NextMediaActionNews: 蘋果日報 - 動新聞
NextTV: 壹電視
Nexx
NexxEmbed
nfl.com (Currently broken)
nfl.com:article (Currently broken)
NhkVod
NhkVodProgram
nhl.com
nick.com
nick.de
nickelodeon:br
nickelodeonru
nicknight
niconico: ニコニコ動画
NiconicoPlaylist
Nintendo
njoy: N-JOY
njoy:embed
NJPWWorld: 新日本プロレスワールド
NobelPrize
NonkTube
Noovo
Normalboots
NosVideo
Nova: TN.cz, Prásk.tv, Nova.cz, Novaplus.cz, FANDA.tv, Krásná.cz and Doma.cz
NovaEmbed
nowness
nowness:playlist
nowness:series
Noz
npo: npo.nl, ntr.nl, omroepwnl.nl, zapp.nl and npo3.nl
npo.nl:live
npo.nl:radio
npo.nl📻fragment
Npr
NRK
NRKPlaylist
NRKRadioPodkast
NRKSkole: NRK Skole
NRKTV: NRK TV and NRK Radio
NRKTVDirekte: NRK TV Direkte and NRK Radio Direkte
NRKTVEpisode
NRKTVEpisodes
NRKTVSeason
NRKTVSeries
NRLTV
ntv.ru
Nuvid
NYTimes
NYTimesArticle
NYTimesCooking
NZZ
ocw.mit.edu
OdaTV
Odnoklassniki
OktoberfestTV
OnDemandKorea
onet.pl
onet.tv
onet.tv:channel
OnetMVP
OnionStudios
Ooyala
OoyalaExternal
OraTV
orf:burgenland: Radio Burgenland
orf:fm4: radio FM4
orf:fm4:story: fm4.orf.at stories
orf:iptv: iptv.ORF.at
orf:kaernten: Radio Kärnten
orf:noe: Radio Niederösterreich
orf:oberoesterreich: Radio Oberösterreich
orf:oe1: Radio Österreich 1
orf:oe3: Radio Österreich 3
orf:salzburg: Radio Salzburg
orf:steiermark: Radio Steiermark
orf:tirol: Radio Tirol
orf:tvthek: ORF TVthek
orf:vorarlberg: Radio Vorarlberg
orf:wien: Radio Wien
OsnatelTV
OutsideTV
PacktPub
PacktPubCourse
PalcoMP3:artist
PalcoMP3:song
PalcoMP3:video
pandora.tv: 판도라TV
ParamountNetwork
parliamentlive.tv: UK parliament videos
Patreon
pbs: Public Broadcasting Service (PBS) and member stations: PBS: Public Broadcasting Service, APT - Alabama Public Television (WBIQ), GPB/Georgia Public Broadcasting (WGTV), Mississippi Public Broadcasting (WMPN), Nashville Public Television (WNPT), WFSU-TV (WFSU), WSRE (WSRE), WTCI (WTCI), WPBA/Channel 30 (WPBA), Alaska Public Media (KAKM), Arizona PBS (KAET), KNME-TV/Channel 5 (KNME), Vegas PBS (KLVX), AETN/ARKANSAS ETV NETWORK (KETS), KET (WKLE), WKNO/Channel 10 (WKNO), LPB/LOUISIANA PUBLIC BROADCASTING (WLPB), OETA (KETA), Ozarks Public Television (KOZK), WSIU Public Broadcasting (WSIU), KEET TV (KEET), KIXE/Channel 9 (KIXE), KPBS San Diego (KPBS), KQED (KQED), KVIE Public Television (KVIE), PBS SoCal/KOCE (KOCE), ValleyPBS (KVPT), CONNECTICUT PUBLIC TELEVISION (WEDH), KNPB Channel 5 (KNPB), SOPTV (KSYS), Rocky Mountain PBS (KRMA), KENW-TV3 (KENW), KUED Channel 7 (KUED), Wyoming PBS (KCWC), Colorado Public Television / KBDI 12 (KBDI), KBYU-TV (KBYU), Thirteen/WNET New York (WNET), WGBH/Channel 2 (WGBH), WGBY (WGBY), NJTV Public Media NJ (WNJT), WLIW21 (WLIW), mpt/Maryland Public Television (WMPB), WETA Television and Radio (WETA), WHYY (WHYY), PBS 39 (WLVT), WVPT - Your Source for PBS and More! (WVPT), Howard University Television (WHUT), WEDU PBS (WEDU), WGCU Public Media (WGCU), WPBT2 (WPBT), WUCF TV (WUCF), WUFT/Channel 5 (WUFT), WXEL/Channel 42 (WXEL), WLRN/Channel 17 (WLRN), WUSF Public Broadcasting (WUSF), ETV (WRLK), UNC-TV (WUNC), PBS Hawaii - Oceanic Cable Channel 10 (KHET), Idaho Public Television (KAID), KSPS (KSPS), OPB (KOPB), KWSU/Channel 10 & KTNW/Channel 31 (KWSU), WILL-TV (WILL), Network Knowledge - WSEC/Springfield (WSEC), WTTW11 (WTTW), Iowa Public Television/IPTV (KDIN), Nine Network (KETC), PBS39 Fort Wayne (WFWA), WFYI Indianapolis (WFYI), Milwaukee Public Television (WMVS), WNIN (WNIN), WNIT Public Television (WNIT), WPT (WPNE), WVUT/Channel 22 (WVUT), WEIU/Channel 51 (WEIU), WQPT-TV (WQPT), WYCC PBS Chicago (WYCC), WIPB-TV (WIPB), WTIU (WTIU), CET (WCET), ThinkTVNetwork (WPTD), WBGU-TV (WBGU), WGVU TV (WGVU), NET1 (KUON), Pioneer Public Television (KWCM), SDPB Television (KUSD), TPT (KTCA), KSMQ (KSMQ), KPTS/Channel 8 (KPTS), KTWU/Channel 11 (KTWU), East Tennessee PBS (WSJK), WCTE-TV (WCTE), WLJT, Channel 11 (WLJT), WOSU TV (WOSU), WOUB/WOUC (WOUB), WVPB (WVPB), WKYU-PBS (WKYU), KERA 13 (KERA), MPBN (WCBB), Mountain Lake PBS (WCFE), NHPTV (WENH), Vermont PBS (WETK), witf (WITF), WQED Multimedia (WQED), WMHT Educational Telecommunications (WMHT), Q-TV (WDCQ), WTVS Detroit Public TV (WTVS), CMU Public Television (WCMU), WKAR-TV (WKAR), WNMU-TV Public TV 13 (WNMU), WDSE - WRPT (WDSE), WGTE TV (WGTE), Lakeland Public Television (KAWE), KMOS-TV - Channels 6.1, 6.2 and 6.3 (KMOS), MontanaPBS (KUSM), KRWG/Channel 22 (KRWG), KACV (KACV), KCOS/Channel 13 (KCOS), WCNY/Channel 24 (WCNY), WNED (WNED), WPBS (WPBS), WSKG Public TV (WSKG), WXXI (WXXI), WPSU (WPSU), WVIA Public Media Studios (WVIA), WTVI (WTVI), Western Reserve PBS (WNEO), WVIZ/PBS ideastream (WVIZ), KCTS 9 (KCTS), Basin PBS (KPBT), KUHT / Channel 8 (KUHT), KLRN (KLRN), KLRU (KLRU), WTJX Channel 12 (WTJX), WCVE PBS (WCVE), KBTC Public Television (KBTC)
PearVideo
PeerTube
People
PerformGroup
periscope: Periscope
periscope:user: Periscope user videos
PhilharmonieDeParis: Philharmonie de Paris
phoenix.de
Photobucket
Picarto
PicartoVod
Piksel
Pinkbike
Pinterest
PinterestCollection
Pladform
Platzi
PlatziCourse
play.fm
player.sky.it
PlayPlusTV
PlayStuff
PlaysTV
Playtvak: Playtvak.cz, iDNES.cz and Lidovky.cz
Playvid
Playwire
pluralsight
pluralsight:course
podomatic
Pokemon
PolskieRadio
PolskieRadioCategory
Popcorntimes
PopcornTV
PornCom
PornerBros
PornHd
PornHub: PornHub and Thumbzilla
PornHubPagedVideoList
PornHubUser
PornHubUserVideosUpload
Pornotube
PornoVoisines
PornoXO
PornTube
PressTV
prosiebensat1: ProSiebenSat.1 Digital
puhutv
puhutv:serie
Puls4
Pyvideo
qqmusic: QQ音乐
qqmusic:album: QQ音乐 - 专辑
qqmusic:playlist: QQ音乐 - 歌单
qqmusic:singer: QQ音乐 - 歌手
qqmusic:toplist: QQ音乐 - 排行榜
QuantumTV
Qub
Quickline
QuicklineLive
R7
R7Article
radio.de
radiobremen
radiocanada
radiocanada:audiovideo
radiofrance
RadioJavan
Rai
RaiPlay
RaiPlayLive
RaiPlayPlaylist
RayWenderlich
RayWenderlichCourse
RBMARadio
RDS: RDS.ca
RedBull
RedBullEmbed
RedBullTV
RedBullTVRrnContent
Reddit
RedditR
RedTube
RegioTV
RENTV
RENTVArticle
Restudy
Reuters
ReverbNation
RICE
RMCDecouverte
RockstarGames
RoosterTeeth
RottenTomatoes
Roxwel
Rozhlas
RTBF
rte: Raidió Teilifís Éireann TV
rte:radio: Raidió Teilifís Éireann radio
rtl.nl: rtl.nl and rtlxl.nl
rtl2
rtl2:you
rtl2:you:series
RTP
RTS: RTS.ch
rtve.es:alacarta: RTVE a la carta
rtve.es:infantil: RTVE infantil
rtve.es:live: RTVE.es live streams
rtve.es:television
RTVNH
RTVS
RUHD
RumbleEmbed
rutube: Rutube videos
rutube:channel: Rutube channels
rutube:embed: Rutube embedded videos
rutube:movie: Rutube movies
rutube:person: Rutube person videos
rutube:playlist: Rutube playlists
RUTV: RUTV.RU
Ruutu
Ruv
safari: safaribooksonline.com online video
safari:api
safari:course: safaribooksonline.com online courses
SAKTV
SaltTV
SampleFocus
Sapo: SAPO Vídeos
savefrom.net
SBS: sbs.com.au
schooltv
screen.yahoo:search: Yahoo screen search
Screencast
ScreencastOMatic
ScrippsNetworks
scrippsnetworks:watch
SCTE
SCTECourse
Seeker
SenateISVP
SendtoNews
Servus
Sexu
SeznamZpravy
SeznamZpravyArticle
Shahid
ShahidShow
Shared: shared.sx
ShowRoomLive
simplecast
simplecast:episode
simplecast:podcast
Sina
sky.it
sky:news
sky:sports
sky:sports:news
skyacademy.it
SkylineWebcams
skynewsarabia:article
skynewsarabia:video
Slideshare
SlidesLive
Slutload
Snotr
Sohu
SonyLIV
soundcloud
soundcloud:playlist
soundcloud:search: Soundcloud search
soundcloud:set
soundcloud:trackstation
soundcloud:user
SoundcloudEmbed
soundgasm
soundgasm:profile
southpark.cc.com
southpark.cc.com:español
southpark.de
southpark.nl
southparkstudios.dk
SpankBang
SpankBangPlaylist
Spankwire
Spiegel
sport.francetvinfo.fr
Sport5
SportBox
SportDeutschland
spotify
spotify:show
Spreaker
SpreakerPage
SpreakerShow
SpreakerShowPage
SpringboardPlatform
Sprout
sr:mediathek: Saarländischer Rundfunk
SRGSSR
SRGSSRPlay: srf.ch, rts.ch, rsi.ch, rtr.ch and swissinfo.ch play sites
stanfordoc: Stanford Open ClassRoom
Steam
Stitcher
StitcherShow
StoryFire
StoryFireSeries
StoryFireUser
Streamable
streamcloud.eu
StreamCZ
StreetVoice
StretchInternet
stv:player
SunPorno
sverigesradio:episode
sverigesradio:publication
SVT
SVTPage
SVTPlay: SVT Play and Öppet arkiv
SVTSeries
SWRMediathek
Syfy
SztvHu
t-online.de
Tagesschau
tagesschau:player
Tass
TBS
TDSLifeway
Teachable
TeachableCourse
teachertube: teachertube.com videos
teachertube:user:collection: teachertube.com user and collection videos
TeachingChannel
Teamcoco
TeamTreeHouse
TechTalks
techtv.mit.edu
ted
Tele13
Tele5
TeleBruxelles
Telecinco: telecinco.es, cuatro.com and mediaset.es
Telegraaf
TeleMB
TeleQuebec
TeleQuebecEmission
TeleQuebecLive
TeleQuebecSquat
TeleQuebecVideo
TeleTask
Telewebion
TennisTV
TenPlay
TF1
TFO
TheIntercept
ThePlatform
ThePlatformFeed
TheScene
TheStar
TheSun
TheWeatherChannel
ThisAmericanLife
ThisAV
ThisOldHouse
TikTok
TikTokUser (Currently broken)
tinypic: tinypic.com videos
TMZ
TMZArticle
TNAFlix
TNAFlixNetworkEmbed
toggle
ToonGoggles
tou.tv
Toypics: Toypics video
ToypicsUser: Toypics user profile
TrailerAddict (Currently broken)
Trilulilu
Trovo
TrovoVod
TruNews
TruTV
Tube8
TubiTv
Tumblr
tunein:clip
tunein:program
tunein:station
tunein:topic
TunePk
Turbo
tv.dfb.de
TV2
tv2.hu
TV2Article
TV2DK
TV2DKBornholmPlay
TV4: tv4.se and tv4play.se
TV5MondePlus: TV5MONDE+
tv5unis
tv5unis:video
tv8.it
TVA
TVANouvelles
TVANouvellesArticle
TVC
TVCArticle
TVer
tvigle: Интернет-телевидение Tvigle.ru
tvland.com
TVN24
TVNet
TVNoe
TVNow
TVNowAnnual
TVNowNew
TVNowSeason
TVNowShow
tvp: Telewizja Polska
tvp:embed: Telewizja Polska
tvp:series
TVPlayer
TVPlayHome
Tweakers
TwitCasting
twitch:clips
twitch:stream
twitch:vod
TwitchCollection
TwitchVideos
TwitchVideosClips
TwitchVideosCollections
twitter
twitter:amplify
twitter:broadcast
twitter:card
udemy
udemy:course
UDNEmbed: 聯合影音
UFCArabia
UFCTV
UKTVPlay
umg:de: Universal Music Deutschland
Unistra
Unity
uol.com.br
uplynk
uplynk:preplay
Urort: NRK P3 Urørt
URPlay
USANetwork
USAToday
ustream
ustream:channel
ustudio
ustudio:embed
Varzesh3
Vbox7
VeeHD
Veoh
Vesti: Вести.Ru
Vevo
VevoPlaylist
VGTV: VGTV, BTTV, FTV, Aftenposten and Aftonbladet
vh1.com
vhx:embed
Viafree
vice
vice:article
vice:show
Vidbit
Viddler
Videa
video.arnes.si: Arnes Video
video.google:search: Google Video search
video.sky.it
video.sky.it:live
VideoDetective
videofy.me
videomore
videomore:season
videomore:video
VideoPress
Vidio
VidLii
vidme
vidme:user
vidme:user:likes
vier: vier.be and vijf.be
vier:videos
viewlift
viewlift:embed
Viidea
viki
viki:channel
vimeo
vimeo:album
vimeo:channel
vimeo:group
vimeo:likes: Vimeo user likes
vimeo:ondemand
vimeo:review: Review pages on vimeo
vimeo:user
vimeo:watchlater: Vimeo watch later list, "vimeowatchlater" keyword (requires authentication)
Vimple: Vimple - one-click video hosting
Vine
vine:user
Viqeo
Viu
viu:ott
viu:playlist
Vivo: vivo.sx
vk: VK
vk:uservideos: VK - User's Videos
vk:wallpost
vlive
vlive:channel
vlive:post
Vodlocker
VODPl
VODPlatform
VoiceRepublic
Voot
VoxMedia
VoxMediaVolume
vpro: npo.nl, ntr.nl, omroepwnl.nl, zapp.nl and npo3.nl
Vrak
VRT: VRT NWS, Flanders News, Flandern Info and Sporza
VrtNU: VrtNU.be
vrv
vrv:series
VShare
VTM
VTXTV
vube: Vube.com
VuClip
VVVVID
VVVVIDShow
VyboryMos
Vzaar
Wakanim
Walla
WalyTV
washingtonpost
washingtonpost:article
wat.tv
WatchBox
WatchIndianPorn: Watch Indian Porn
WDR
wdr:mobile
WDRElefant
WDRPage
Webcaster
WebcasterFeed
WebOfStories
WebOfStoriesPlaylist
Weibo
WeiboMobile
WeiqiTV: WQTV
Wistia
WistiaPlaylist
wnl: npo.nl, ntr.nl, omroepwnl.nl, zapp.nl and npo3.nl
WorldStarHipHop
WSJ: Wall Street Journal
WSJArticle
WWE
XBef
XboxClips
XFileShare: XFileShare based sites: Aparat, ClipWatching, GoUnlimited, GoVid, HolaVid, Streamty, TheVideoBee, Uqload, VidBom, vidlo, VidLocker, VidShare, VUp, WolfStream, XVideoSharing
XHamster
XHamsterEmbed
XHamsterUser
xiami:album: 虾米音乐 - 专辑
xiami:artist: 虾米音乐 - 歌手
xiami:collection: 虾米音乐 - 精选集
xiami:song: 虾米音乐
ximalaya: 喜马拉雅FM
ximalaya:album: 喜马拉雅FM 专辑
XMinus
XNXX
Xstream
XTube
XTubeUser: XTube user profile
Xuite: 隨意窩Xuite影音
XVideos
XXXYMovies
Yahoo: Yahoo screen and movies
yahoo:gyao
yahoo:gyao:player
yahoo:japannews: Yahoo! Japan News
YandexDisk
yandexmusic:album: Яндекс.Музыка - Альбом
yandexmusic🧑‍🎨albums: Яндекс.Музыка - Артист - Альбомы
yandexmusic🧑‍🎨tracks: Яндекс.Музыка - Артист - Треки
yandexmusic:playlist: Яндекс.Музыка - Плейлист
yandexmusic:track: Яндекс.Музыка - Трек
YandexVideo
YapFiles
YesJapan
yinyuetai:video: 音悦Tai
Ynet
YouJizz
youku: 优酷
youku:show
YouNowChannel
YouNowLive
YouNowMoment
YouPorn
YourPorn
YourUpload
youtube: YouTube.com
youtube:favorites: YouTube.com favourite videos, ":ytfav" for short (requires authentication)
youtube:history: Youtube watch history, ":ythistory" for short (requires authentication)
youtube:playlist: YouTube.com playlists
youtube:recommended: YouTube.com recommended videos, ":ytrec" for short (requires authentication)
youtube:search: YouTube.com searches
youtube:search:date: YouTube.com searches, newest videos first
youtube:subscriptions: YouTube.com subscriptions feed, "ytsubs" keyword (requires authentication)
youtube:tab: YouTube.com tab
youtube:watchlater: Youtube watch later list, ":ytwatchlater" for short (requires authentication)
YoutubeYtBe
YoutubeYtUser
Zapiks
Zattoo
ZattooLive
ZDF
ZDFChannel
Zhihu
zingmp3: mp3.zing.vn
zingmp3:album
zoom
Zype
'''


def get_supported_site():
    d = supported_sites.split("\n")
    return d