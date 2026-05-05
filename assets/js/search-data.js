// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-bookshelf",
          title: "bookshelf",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/books/";
          },
        },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-pokedex",
          title: "pokedex",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/pokedex/";
          },
        },{id: "post-samsara-notes",
        
          title: "Samsara notes",
        
        description: "notes on various interviews with Sanjit of Samsara",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/samsara-seqoia/";
          
        },
      },{id: "books-chip-war",
          title: 'Chip War',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2023/chip_war/";
            },},{id: "books-the-left-hand-of-darkness",
          title: 'The Left Hand of Darkness',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2024/left_hand_of_darkness/";
            },},{id: "books-remarkably-bright-creatures",
          title: 'Remarkably Bright Creatures',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2024/remarkably_bright_creatures/";
            },},{id: "books-tomorrow-and-tomorrow-and-tomorrow",
          title: 'Tomorrow, and Tomorrow, and Tomorrow',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2024/tomorrow_and_tomorrow_and_tomorrow/";
            },},{id: "books-a-gentleman-in-moscow",
          title: 'A Gentleman in Moscow',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/a_gentleman_in_moscow/";
            },},{id: "books-angels-and-demons",
          title: 'Angels and Demons',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/angels_and_demons/";
            },},{id: "books-children-of-time",
          title: 'Children of Time',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/children_of_time/";
            },},{id: "books-crying-in-h-mart",
          title: 'Crying in H Mart',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/crying_in_h_mart/";
            },},{id: "books-lin-manuel-miranda-an-education",
          title: 'Lin Manuel Miranda: An Education',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/lin_manuel_miranda_an_education/";
            },},{id: "books-masters-of-command",
          title: 'Masters of Command',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/masters_of_command/";
            },},{id: "books-recursion",
          title: 'Recursion',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/recursion/";
            },},{id: "books-running-with-purpose",
          title: 'Running with Purpose',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/running_with_purpose/";
            },},{id: "books-the-dispossessed",
          title: 'The Dispossessed',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_dispossessed/";
            },},{id: "books-the-farthest-shore",
          title: 'The Farthest Shore',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_farthest_shore/";
            },},{id: "books-the-forever-war",
          title: 'The Forever War',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_forever_war/";
            },},{id: "books-the-poppy-war",
          title: 'The Poppy War',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_poppy_war/";
            },},{id: "books-the-thinking-machine-nvidia",
          title: 'The Thinking Machine (NVIDIA)',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_thinking_machine_nvidia/";
            },},{id: "books-the-tombs-of-atuan",
          title: 'The Tombs of Atuan',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2025/the_tombs_of_atuan/";
            },},{id: "books-siddhartha",
          title: 'Siddhartha',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2026/Siddartha/";
            },},{id: "books-the-surrender-experiment",
          title: 'The Surrender Experiment',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/2026/SurrenderExp/";
            },},{id: "books-this-is-how-you-lose-the-time-war",
          title: 'This Is How You Lose the Time War',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/art/this_is_how_you_lose_the_time_war/";
            },},{id: "books-everything-is-tuberculosis",
          title: 'Everything is Tuberculosis',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/mental_models/everything_is_tuberculosis/";
            },},{id: "books-the-empire-of-ai",
          title: 'The Empire of AI',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/mental_models/the_empire_of_ai/";
            },},{id: "books-a-fire-upon-the-deep",
          title: 'A Fire Upon the Deep',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/rent-free/a_fire_upon_the_deep/";
            },},{id: "news-a-simple-inline-announcement",
          title: 'A simple inline announcement.',
          description: "",
          section: "News",},{id: "news-a-long-announcement-with-details",
          title: 'A long announcement with details',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/announcement_2/";
            },},{id: "news-a-simple-inline-announcement-with-markdown-emoji-sparkles-smile",
          title: 'A simple inline announcement with Markdown emoji! :sparkles: :smile:',
          description: "",
          section: "News",},{id: "projects-project-1",
          title: 'project 1',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-project-2",
          title: 'project 2',
          description: "a project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-project-3-with-very-long-name",
          title: 'project 3 with very long name',
          description: "a project that redirects to another website",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-project-4",
          title: 'project 4',
          description: "another without an image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-project-5",
          title: 'project 5',
          description: "a project with a background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-project-6",
          title: 'project 6',
          description: "a project with no image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "projects-project-7",
          title: 'project 7',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_project/";
            },},{id: "projects-project-8",
          title: 'project 8',
          description: "an other project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/8_project/";
            },},{id: "projects-project-9",
          title: 'project 9',
          description: "another project with an image 🎉",
          section: "Projects",handler: () => {
              window.location.href = "/projects/9_project/";
            },},{
        id: 'social-cv',
        title: 'CV',
        section: 'Socials',
        handler: () => {
          window.open("/assets/pdf/example_pdf.pdf", "_blank");
        },
      },{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%79%6F%75@%65%78%61%6D%70%6C%65.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-inspire',
        title: 'Inspire HEP',
        section: 'Socials',
        handler: () => {
          window.open("https://inspirehep.net/authors/1010907", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=qc6CJjYAAAAJ", "_blank");
        },
      },{
        id: 'social-custom_social',
        title: 'Custom_social',
        section: 'Socials',
        handler: () => {
          window.open("https://www.alberteinstein.com/", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
