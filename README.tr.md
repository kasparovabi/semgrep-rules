# Yayınlanmış güvenlik bildirimlerinden Semgrep kuralları

[English](README.md)

Bildirdiğim ve bakımcıların yayınladığı güvenlik açıklarının ardındaki hata sınıfları için Semgrep kuralları. Her sınıfın yanında kendi kodunuzu nasıl koruyacağınıza dair kısa bir rehber var. Açıkların teknik yazıları [kasparovabi/security-research](https://github.com/kasparovabi/security-research) deposunda.

Burada yalnızca yayınlanmış ve düzeltilmiş açıklar kullanılır. Hâlâ gizli incelemede olan bildirimler kurallarda, testlerde ve bu metinde yer almaz.

## Dizin yapısı

```
rules/<dil>/<sınıf>.yaml    kurallar
tests/<dil>/<sınıf>.<uzantı> semgrep --test için olumlu (ruleid) ve olumsuz (ok) örnekler
```

## Kullanım

Bir projeyi taramak için

```sh
docker run --rm --network none -v "$PWD":/src semgrep/semgrep \
  semgrep --metrics off --config /kurallarin/yolu /src
```

ya da yerel kurulumla `semgrep --config rules/ proje/yolu`.

Testleri çalıştırmak için

```sh
./test.sh
```

SQL testlerinde `-- # ruleid:` yorumları kullanılır, çünkü `semgrep --test` yalnızca `#` ve `//` ile başlayan işaretleri okur.

Kural listesi ve ilgili advisory bağlantıları için [İngilizce README](README.md#rules) tablosuna bakın.

## Nasıl korunursunuz

### Yerel sunucularda DNS rebinding

127.0.0.1 adresine bağlanan bir sunucuya başka makineler ulaşamaz, ama aynı makinedeki tarayıcı ulaşabilir. Kendi alan adını 127.0.0.1'e yeniden çözdüren bir sayfa tarayıcının gözünde aynı kökendendir ve yanıtları okuyabilir. Onu ele veren tek şey `Host` başlığıdır. GET dahil her istekte `Host` başlığını dinlediğiniz adlarla karşılaştırın, `Origin` geldiğinde onu da denetleyin. Rastgele port saldırganı yalnızca yavaşlatır. Sır döndüren ya da kullanıcının kimlik bilgileriyle başka bir sisteme vekillik eden yolları önce test edin. Resmi SDK'larla yazılmış MCP sunucularında taşıma katmanının DNS rebinding korumasını açın ve izinli host listesini verin.

Advisory [KSail GHSA-g57x-rm7r-hf26](https://github.com/devantler-tech/ksail/security/advisories/GHSA-g57x-rm7r-hf26), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-10-ksail-webui-dns-rebinding.md).

### Loopback API'de CORS

`allow_origins=["*"]` herkese açık ve salt okunur bir API için makul olabilir. Özel veri tutan yerel bir API'de ise kullanıcının tarayıcısındaki her sayfa bu veriyi okuyabilir. Karşı tarafın adresine bakmak işe yaramaz, çünkü tarayıcı da bir loopback istemcisidir. CORS listesini varsayılan olarak boş bırakın ve yalnızca erişmesi gereken kökenleri ekleyin. API kimlik doğrulamasızsa listede olmayan `Origin` ile gelen ve loopback adı taşımayan `Host` ile gelen istekleri reddedin. Origin denetimi siteler arası istekleri, Host denetimi rebinding saldırısını durdurur.

Advisory [mnemo-cortex GHSA-682p-grrx-wrwg](https://github.com/GuyMannDude/mnemo-cortex/security/advisories/GHSA-682p-grrx-wrwg), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-10-mnemo-cortex-cors-loopback.md).

### Uygulanmayan izinli dizin sınırı

Belgelerdeki güvenlik ayarlarına kullanıcılar güvenir, bu yüzden `--allow-dir` gibi bir bayrağı kodun gerçekten uygulaması gerekir. Tanınmayan bir bayrakta program hata verip durmalı. Modelden gelen her yolu sembolik bağlantıları izleyerek çözün ve izinli köklerden birinin altında kalmıyorsa reddedin. Bu denetimi yol alan bütün araçların çağırdığı tek bir fonksiyona koyun ve her aracı kök dışındaki bir yolla çalıştıran bir test ekleyin. Denetim en çok yeni eklenen araçlarda unutulur. Kaynak kodun yanında kullanıcıların kurduğu paketi de test edin.

Advisory [anymd GHSA-qr3f-g5wf-225w](https://github.com/SylphxAI/anymd/security/advisories/GHSA-qr3f-g5wf-225w), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-09-anymd-allow-dir-not-implemented.md).

### Girdiden boyutlanan bellek ayırma

Dosyadan ya da istekten okunan bir sayıyı doğrudan `Vec::with_capacity`, `reserve` ya da `vec![x; n]` çağrısına vermeyin. Rust'ta başarısız bir bellek ayırma süreci sonlandırır ve `catch_unwind` bunu durduramaz, böylece tek bir dosya sunucudaki bütün oturumları bitirebilir. Sayıyı kalan girdinin gerçekten tarif edebileceği miktarla sınırlayın, örneğin kalan bayt sayısını en küçük kayıt boyutuna bölerek. Kayıt başına sabit bir üst sınır, kayıt sayısı arttıkça yine büyük bir toplama ulaşır. Yalnızca bir döngüyü süren sayılara da aynı denetimi uygulayın, onlar çökme yerine takılmaya yol açar.

Advisory [altium-designer-mcp GHSA-p2qw-h8m7-5x69](https://github.com/embedded-society/altium-designer-mcp/security/advisories/GHSA-p2qw-h8m7-5x69), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-10-altium-designer-mcp-unbounded-allocation.md).

### Supabase ve Postgres satır düzeyi güvenliği (RLS)

Anon anahtarı her istemci paketine gömülür, veriyi koruyan şey RLS politikalarıdır. Postgres izin veren (permissive) politikaları OR ile birleştirir. Bu yüzden `anon` ya da `PUBLIC` için yazılmış tek bir `USING (true)` politikası, diğer politikalar ne kadar dar olursa olsun bütün tabloyu açar. Her rol ve komut için en geniş izin veren politikayı arayın ve son durumu görmek için migration dosyalarını sırasıyla uygulayın. E-posta gibi kişisel sütunları anonim okuma yolu olmayan tablolarda tutun. Canlı veritabanında depoda görünmeyen politikalar olabileceğini de unutmayın.

Advisory [asset-intel-orchestration-engine GHSA-8h52-3cfj-cmrw](https://github.com/Kronova-Intelligent-Systems/asset-intel-orchestration-engine/security/advisories/GHSA-8h52-3cfj-cmrw), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-09-kronova-profiles-rls.md).

### SQL'in salt okunur olduğuna anahtar kelime listesiyle karar vermek

Yazma fiillerinden oluşan bir yasak listesi bir sorgunun yazıp yazmadığını söyleyemez. `SELECT ... INTO` PostgreSQL'de tablo oluşturur, `SELECT ... INTO OUTFILE` MySQL sunucusunda dosya yazar ve her lehçede başka yollar da vardır. Sorguyu ayrıştırın, yalnızca küçük bir okuma dilbilgisini kabul edin, geri kalan her şeyi onay gerektiren yazma sayın. İkinci katman olarak salt okunur oturumları salt okunur bir işlem (transaction) içinde çalıştırın. Ayrıştırmaya bağlı olmayan sınır için `CREATE` ve `FILE` yetkisi olmayan bir veritabanı hesabı kullanın.

Advisory [WhoDB GHSA-pvf2-6h4x-r24j](https://github.com/clidey/whodb/security/advisories/GHSA-pvf2-6h4x-r24j), yazı [burada](https://github.com/kasparovabi/security-research/blob/main/2026-09-whodb-select-into.md).

### Python 3.12 ve 3.13'te kaldırılan modüller

Python 3.13, PEP 594'te listelenen modülleri kaldırdı (`cgi`, `pipes`, `telnetlib`, `audioop`, `crypt`, `imghdr` ve diğerleri). 3.12 ise `asyncore`, `asynchat`, `smtpd`, `imp` ve `distutils` modüllerini kaldırdı. Bunları içe aktaran kod daha açılışta hata verir, çoğu zaman da kimsenin gerekene kadar çalıştırmadığı betiklerde. Kullanılmayan içe aktarmaları silin, kalanları değiştirin (`pipes.quote` yerine `shlex.quote`, `cgi.escape` yerine `html.escape`, `audioop` için `audioop-lts` paketi). Eski ve yeni sürümleri birlikte desteklemeniz gerekiyorsa içe aktarmayı `try/except ImportError` ile koruyun. Bu sınıf uyumlulukla ilgilidir. Bu çalışmadan çıkan ve birleştirilen düzeltmeler [security-research README](https://github.com/kasparovabi/security-research#merged-fixes-in-other-projects) içinde listeleniyor.

## Sınırlar

Bu kurallar sezgiseldir. Bazıları Semgrep'in göremediği bağlama ihtiyaç duyar (örneğin başka bir ara katmanda yapılan Host denetimi), bu yüzden her bulguyu bakılacak bir yer olarak ele alın. Taint kuralları veriyi yalnızca tek bir fonksiyon içinde izler. Yanlış pozitif ya da kaçırılan durumlar için issue ve pull request açabilirsiniz.

## Lisans

MIT, ayrıntı için [LICENSE](LICENSE).
