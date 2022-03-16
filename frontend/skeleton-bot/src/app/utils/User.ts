export class User {
  constructor (id: string, avatar: string, discriminator: string, username: string) {
      this.id = id;
      this.avatar = "https://cdn.discordapp.com/avatars/" + id + "/" + avatar + ".png";
      this.discriminator = discriminator;
      this.username = username;
  }
    id: string;
    avatar: string;
    discriminator: string;
    username: string;
    guilds: string[];
}