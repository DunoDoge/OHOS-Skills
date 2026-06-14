// ObjectLiteralInterfaceError.ets - declare interface before literal
// BAD: untyped literal
// const card = { id: 1, name: 'Alice' }; // arkts-no-untyped-obj-literals

// GOOD
interface UserCard {
  id: number;
  name: string;
  avatar: ResourceStr;
}

const card: UserCard = {
  id: 1,
  name: 'Alice',
  avatar: $r('app.media.avatar')
};

function render(c: UserCard): string {
  return `${c.id}-${c.name}`;
}

export const tag: string = render(card);
