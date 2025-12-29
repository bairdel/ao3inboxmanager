import re
import regex
string = """
      Archive of Our Own
      =========================================


      Thisisentertaining (https://archiveofourown.org/users/Thisisentertaining/pseuds/Thisisentertaining) posted a new work:
      https://archiveofourown.org/works/76374946

      "Instincts at Sea" (2999 words)
      by Thisisentertaining (https://archiveofourown.org/users/Thisisentertaining/pseuds/Thisisentertaining)


      Chapters: 1/?
      Fandom: Avatar: The Last Airbender (Cartoon 2005)    
      Rating: Teen And Up Audiences
      Warning: Graphic Depictions Of Violence
      Relationships: The Gaang & Zuko (Avatar), Katara & Zuko (Avatar), Mentioned Hakoda/Kya - Relationship
      Characters: Zuko (Avatar), Katara (Avatar), Aang (Avatar), Sokka (Avatar), Toph Beifong, Hakoda (Avatar), Bato (Avatar), Yon Rha (Avatar), Yon Rha's Mother (Avatar), Pipsqueak (Avatar), The Duke (Avatar)
      Additional Tags: Book 3: Fire (Avatar), Fire Nation Navy, Southern Water Tribe, Lack of Communication, Grief/Mourning, Post-Traumatic Stress Disorder - PTSD, Zuko is not having a good time, Katara is not having a good time, southern raiders
      Series: Part 18 of Always trust Sokka's instincts    



      Summary:
          With Ba Sing Se in control of the Fire Nation, the GAang no longer have an elite Earth Kingdom army at their back. Luckily, they have an elite Water Tribe navy just outside of the city. However, being among the Water Tribe, and their two new recruits, is bringing up the past in unexpected ways. Not to mention that the events of the last few days in Ba Sing Se have paid a toll on all of them, especially Zuko.


      For now though, they have no choice but to endure it as they take their voyage and wait for Aang to awake... with a possible field trip here and there.


      -----------------------------------------
      You're receiving this email because you've subscribed to Always trust Sokka's instincts. Follow the link to unsubscribe if you no longer wish to receive updates: https://archiveofourown.org/series/1883224


      If you don't understand why you received this email, please contact Support: https://archiveofourown.org/support.

      The Archive of Our Own is a fan-run and fan-supported archive that relies on your donations: https://archiveofourown.org/donate.
      """

pattern = regex.compile(r'\bChapters:\s+\K\S+')
chapters = regex.findall(pattern,string)
print(chapters)