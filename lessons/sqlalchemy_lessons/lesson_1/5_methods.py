# user = User(**data)  # transient
#
# session.add(user)  # pending
#
# session.flush() \ session.commit()  # persistent
#
#
# user: User = select(User).where(User.id = id_) # detached
# session.close()
#
# session.delete(user)  # deleted
# session.commit()