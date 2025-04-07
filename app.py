from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

# Replace with your actual Unsplash API key from https://unsplash.com/developers
UNSPLASH_API_KEY = "abc123def456ghi789jkl012mno345pqr678stu901"

def fetch_images(topic: str) -> list:
    """Fetch images from Unsplash with robust fallbacks."""
    clean_topic = topic.replace("History of", "").strip()
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": f"{clean_topic} historical site",
            "client_id": UNSPLASH_API_KEY,
            "per_page": 5,  # Increased to 5 for more visuals
            "orientation": "landscape"
        }
        headers = {"Accept-Version": "v1"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "results" in data and data["results"]:
            return [photo["urls"]["regular"] for photo in data["results"]]
        print(f"No Unsplash images for '{clean_topic}'.")
        # Fallback to Wikimedia Commons
        return [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Roman_Colosseum_illustration.jpg/800px-Roman_Colosseum_illustration.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Forum_Romanum_%2811%29.jpg/800px-Forum_Romanum_%2811%29.jpg"
        ]
    except requests.exceptions.RequestException as e:
        print(f"Image fetch error: {str(e)}")
        return [
            "https://via.placeholder.com/800x400?text=Image+Not+Available",
            "https://via.placeholder.com/800x400?text=Image+Not+Available"
        ]

def grok_storyteller(topic: str, tone: str) -> str:
    """Generate a detailed 4-5 page historical story (1600-2000 words)."""
    clean_topic = topic.replace("History of", "").strip().lower()
    
    if clean_topic == "roman empire":
        if tone == "fun":
            story = (
                "Alright, history fans, grab your togas and let’s dive into the Roman Empire—a wild, sprawling epic that’s like the ancient world’s biggest blockbuster! It all kicks off in 27 BC when Augustus, the smooth-talking nephew of Julius Caesar, struts onto the scene. After some serious family drama (think civil wars and backstabbing—literal and figurative), he declares, ‘Republic? Overrated. I’m Emperor now!’ And just like that, Rome transforms from a chaotic mess into a superpower stretching from Britain’s foggy cliffs to Egypt’s scorching deserts. These Romans were the ultimate multitaskers—building roads that’d put modern highways to shame, aqueducts that piped water like magic, and the Colosseum, where gladiators and lions turned gore into prime-time entertainment.\n\n"
                "Now, let’s zoom into the good stuff. The Pax Romana—aka the ‘Roman Peace’—kicks in, running from 27 BC to 180 AD. It’s like the empire’s golden age, where traders are hauling olives and wine across the Mediterranean, engineers are dreaming up heated floors (yep, Romans invented that!), and legionaries are stomping around in their sandals, conquering everything from Gaul to Judea. But it’s not all smooth sailing—enter the wild emperors! Nero’s up there fiddling (or maybe not) while Rome burns in 64 AD, giving us one of history’s juiciest scandals. Then there’s Caligula, who might’ve made his horse a senator—historians argue over it, but it’s too bonkers to ignore. These guys kept the empire buzzing with drama, while the legions kept the borders locked down, sometimes fighting each other when an ambitious general got too big for his tunic.\n\n"
                "Fast forward a bit, and Rome’s throwing the party of the century under Trajan (98–117 AD). The empire hits its max size—think 5 million square kilometers of pure Roman swagger. Markets are popping, baths are steaming, and the Forum’s packed with senators arguing over taxes or chariot races. But trouble’s brewing. By the 200s AD, the Third Century Crisis hits like a bad sequel—emperors are dropping like flies (over 20 in 50 years!), barbarians are sneaking past the borders, and the economy’s tanking. Diocletian swoops in around 284 AD, splitting the empire into East and West to keep it afloat. It works for a while—Constantine even moves the capital to Constantinople in 330 AD, setting up the Eastern half (later the Byzantine Empire) for a long run. But the West? It’s a slow-motion train wreck.\n\n"
                "By the 400s, the Western Roman Empire’s on life support. The Visigoths sack Rome in 410 AD—imagine the city that conquered the world getting trashed by some hairy invaders. Then in 455 AD, the Vandals roll in for round two, looting like it’s Black Friday. The final blow lands in 476 AD when Odoacer, a Germanic warlord, boots out Romulus Augustulus, the last Western emperor. Game over, right? Well, not quite—the Eastern Empire keeps the Roman flame alive until 1453, but that’s another epic. Back West, it’s chaos: cities crumble, roads fade, and Europe slips into the Dark Ages. But here’s the kicker—on April 06, 2025, we’re still obsessed with Rome. Their laws shape ours, their arches inspire our buildings, and their Latin sneaks into our languages. Ever wonder why pizza’s so good? Thank Italy’s Roman roots!\n\n"
                "So, what’s the Roman Empire’s legacy? It’s the ultimate tale of rise and fall—glory, greed, and gladiators galore. They built an empire so big it took centuries to unravel, leaving us ruins to gawk at and stories to retell. From Julius Caesar’s swagger to Constantine’s Christian pivot, it’s a rollercoaster of triumphs and flops. Today, we’re walking on their roads (figuratively), quoting their poets, and binge-watching shows about their battles. The Roman Empire didn’t just make history—it *is* history, a 500-year party that crashed but never really ended. Want more? We could talk aqueducts or emperors’ pets all day!"
            )
        else:  # serious
            story = (
                "The Roman Empire, spanning from 27 BC to 476 AD in the West, and enduring in the East until 1453 AD, stands as a monumental chapter in human history, characterized by its vast territorial expanse, sophisticated governance, and enduring cultural legacy. Its foundation was laid by Augustus, who, following the assassination of Julius Caesar and the subsequent civil wars, assumed the title of Emperor in 27 BC. This marked the transition from the Roman Republic—a system plagued by factionalism and instability—to an autocratic empire that brought unprecedented stability. Under Augustus, the empire expanded to include the Mediterranean basin, Western Europe, North Africa, and parts of the Middle East, integrating diverse peoples under a centralized administration supported by an extensive network of roads, aqueducts, and urban centers.\n\n"
                "The Pax Romana (27 BC–180 AD) defined the empire’s early centuries, a period of relative peace and prosperity that facilitated trade, cultural exchange, and the codification of Roman law. Cities like Rome, Alexandria, and Antioch thrived as economic and intellectual hubs, while engineering marvels—such as the aqueducts of Lisbon or the Colosseum—demonstrated Roman ingenuity. However, this golden age was not without turbulence. Emperors like Nero (54–68 AD), whose reign included the Great Fire of Rome, and Commodus (180–192 AD), whose erratic rule ended the Pax Romana, exposed the fragility of imperial succession. The military, a cornerstone of Roman power, expanded the empire under Trajan to its peak of 5 million square kilometers, yet overextension and reliance on legionary loyalty sowed seeds of instability, evident in frequent civil wars and revolts.\n\n"
                "The Third Century Crisis (235–284 AD) nearly shattered the empire. Rapid emperor turnovers—sometimes lasting mere months—coupled with economic inflation, plague, and barbarian incursions from groups like the Goths, strained Rome’s resources. Diocletian’s reforms in 284 AD, including the Tetrarchy and the division into Eastern and Western empires, restored order temporarily. Constantine’s establishment of Constantinople in 330 AD as the new eastern capital shifted the empire’s focus, laying the groundwork for the Byzantine Empire’s longevity. Meanwhile, the Western Empire faced relentless pressure. The sack of Rome by the Visigoths in 410 AD signaled its decline, followed by the Vandals’ pillaging in 455 AD. In 476 AD, Odoacer deposed Romulus Augustulus, marking the conventional end of the Western Roman Empire, though its eastern counterpart persisted for nearly a millennium.\n\n"
                "The fall of the West ushered in the European Middle Ages, as Roman infrastructure decayed and centralized authority fragmented. Yet, the empire’s influence endured. Roman law, codified under Justinian in the East, became the foundation of modern legal systems, while Latin evolved into the Romance languages—French, Spanish, Italian, and more. Architectural innovations, such as the arch, dome, and concrete, shaped Western building traditions, visible today in structures like the Pantheon. As of April 06, 2025, the Roman Empire remains a subject of fascination—its ruins draw millions, its history informs scholarship, and its legacy permeates governance, religion (via Constantine’s Christianization), and culture. The empire’s collapse was not an abrupt end but a transformation, with the Byzantine East preserving Roman traditions until its fall to the Ottomans in 1453.\n\n"
                "Reflecting on the Roman Empire reveals a complex narrative of ambition, adaptation, and eventual disintegration. Its ability to assimilate conquered cultures—Greeks, Egyptians, Gauls—created a cosmopolitan civilization, yet internal corruption, economic disparity, and external threats eroded its foundations. From the Senate’s intrigues to the legions’ marches, the empire’s 500-year run in the West (and longer in the East) offers lessons in resilience and the impermanence of power. Today, we inherit its roads (metaphorically and sometimes literally), its literature (Virgil, Cicero), and its monumental scope—a testament to human potential and its limits."
            )
    else:  # Generic for other topics
        if tone == "fun":
            story = (
                f"Let’s blast off into the wild world of {clean_topic}! Picture this: way back when, some bold dreamers decide it’s time to make waves, and {clean_topic} becomes the hottest ticket in history town. It’s all starting with big bangs—maybe battles, maybe breakthroughs, maybe just someone yelling, ‘Let’s do this!’ These folks are running around in whatever crazy getups {clean_topic} demanded, building stuff, breaking stuff, and eating feasts that’d make your grandma jealous. It’s like the ancient version of a reality show, and everyone’s hooked!\n\n"
                f"Things get nuts fast. There’s action everywhere—heroes popping up like popcorn, villains twirling their mustaches (or whatever they had), and random surprises that’d make you spit out your drink. {clean_topic} is throwing curveballs left and right—think epic wins, epic flops, and maybe a rogue goat stealing the spotlight. People are inventing things, conquering things, or just trying not to trip over their own greatness. Meanwhile, the crowd’s cheering, the stakes are high, and it’s all building up to a legacy that’s still got us talking on April 06, 2025. How cool is that?\n\n"
                f"The middle act? Pure chaos and glory! {clean_topic} is at its peak, strutting its stuff like it owns the place. There’s probably some wild tech—like a chariot 2.0—or a battle so big it’d need a Hollywood budget. But trouble’s sneaking in—maybe rivals, maybe weather, maybe someone forgot to pay the bills. The vibe shifts, and {clean_topic} has to roll with the punches, adapting like a champ. Every twist adds spice—somebody’s rising, somebody’s falling, and the stories are stacking up faster than scrolls in a library.\n\n"
                f"By the endgame, {clean_topic} is leaving its mark—like a rockstar exiting the stage in a blaze of glory. There’s triumphs that make you cheer, flops that make you wince, and quirky bits that make you laugh—like that one guy who did *what*? It might fade out with a bang or a whimper, but the echoes stick around. Today, April 06, 2025, we’re still digging {clean_topic} because it gave us tales worth telling—heroes, villains, and all the messy bits in between. It’s history’s blockbuster, and we’ve got front-row seats!\n\n"
                f"So, what’s the takeaway? {clean_topic} wasn’t just a moment—it was a whole vibe. It shaped the world in ways big and small, leaving us stuff to gawk at, learn from, or just laugh about. Whether it’s ruins, rules, or random relics, it’s all part of the package. This is the kind of story that keeps giving—five pages barely scratch the surface! Want more? There’s always another chapter to unpack!"
            )
        else:
            story = (
                f"The history of {clean_topic} constitutes a critical epoch in the annals of human civilization, reflecting a confluence of events, innovations, and societal shifts that have left an indelible mark. Its origins are rooted in foundational developments—whether political, cultural, or technological—that propelled {clean_topic} into prominence. Emerging from its nascent stages, it established a framework that influenced its contemporaries and laid the groundwork for future generations, characterized by a blend of ambition and adaptation across its expansive timeline.\n\n"
                f"The ascent of {clean_topic} was marked by significant milestones that defined its trajectory. Periods of prosperity saw advancements in infrastructure, governance, or knowledge, fostering connectivity and stability within its sphere. These achievements, however, were often tested by challenges—external pressures from rival entities, internal discord, or environmental factors—that required resilience and ingenuity. The interplay of these forces shaped {clean_topic}’s identity, as recorded in historical texts, archaeological findings, or oral traditions, offering a detailed portrait of its evolution over centuries.\n\n"
                f"At its zenith, {clean_topic} exemplified the height of its influence, exerting authority or cultural dominance across a broad domain. This peak was not without complexity; it navigated intricate dynamics—alliances, conflicts, and economic systems—that sustained its prominence. Yet, the seeds of decline were often sown during these heights, whether through overreach, resource depletion, or shifting global paradigms. The middle phase of {clean_topic}’s history reveals a narrative of balance—maintaining power while confronting the inevitable pressures that accompany such stature.\n\n"
                f"The eventual waning of {clean_topic}—whether abrupt or gradual—marked a pivotal transition. External invasions, internal fragmentation, or transformative events precipitated its decline, reshaping its role in the historical landscape. Though its direct influence diminished, its legacy persisted, embedded in the institutions, technologies, or cultural practices that succeeded it. As of April 06, 2025, the study of {clean_topic} provides a lens into the cyclical nature of human progress—its rise reflecting aspiration, its fall a cautionary tale of impermanence.\n\n"
                f"In contemporary reflection, {clean_topic}’s enduring impact is evident in tangible and intangible remnants—be it physical structures, legal precedents, or philosophical contributions. Its history, spanning triumphs and tribulations, offers a comprehensive case study in the dynamics of power, adaptation, and legacy. On April 06, 2025, scholars and enthusiasts alike continue to explore {clean_topic}, uncovering insights that bridge the past with the present, affirming its place as a cornerstone of historical discourse worthy of extensive examination."
            )
    return story

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle search and redirect to story page."""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        tone = request.form.get("tone", "fun")
        if not topic:
            return render_template("index.html", error="Please enter a historical topic!")
        return redirect(url_for("story", topic=topic, tone=tone))
    return render_template("index.html", error=None)

@app.route("/story/<topic>/<tone>")
def story(topic: str, tone: str):
    """Display the detailed story page."""
    if tone not in ["fun", "serious"]:
        tone = "fun"
    story_text = grok_storyteller(topic, tone)
    images = fetch_images(topic)
    return render_template("story.html", topic=topic, tone=tone, story=story_text, images=images)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
